import yaml
import os
import hashlib
import logging
from . import db
from .models import MigrationLog
from sqlalchemy import text

logger = logging.getLogger(__name__)

class MigrationManager:
    def __init__(self, changelog_path='changelog.yaml'):
        self.changelog_path = changelog_path
        self.migrations = self.load_changelog()
    
    def load_changelog(self):
        """Load and parse changelog file"""
        try:
            with open(self.changelog_path, 'r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            logger.error(f"Error loading changelog: {str(e)}")
            raise
    
    def calculate_checksum(self, file_path):
        """Calculate SHA-256 checksum of migration file"""
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                return hashlib.sha256(content.encode()).hexdigest()
        except Exception as e:
            logger.error(f"Error calculating checksum for {file_path}: {str(e)}")
            raise
    
    def get_executed_migrations(self):
        """Get already executed migrations from database"""
        try:
            # Create migrations_log table if it doesn't exist
            db.create_all()
            
            executed_migrations = MigrationLog.query.order_by(
                MigrationLog.migration_id
            ).all()
            
            return {mig.migration_id: mig for mig in executed_migrations}
        except Exception as e:
            logger.error(f"Error fetching executed migrations: {str(e)}")
            raise
    
    def execute_migration(self, file_path):
        """Execute SQL migration file"""
        try:
            with open(file_path, 'r') as file:
                sql_content = file.read()
            
            # Split SQL statements and execute them
            statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
            
            for statement in statements:
                if statement:
                    db.session.execute(text(statement))
            
            db.session.commit()
            logger.info(f"Successfully executed migration: {file_path}")
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error executing migration {file_path}: {str(e)}")
            raise
    
    def run_migrations(self):
        """Run all pending migrations"""
        logger.info("Starting migration process...")
        
        try:
            executed_migrations = self.get_executed_migrations()
            
            for migration in self.migrations:
                mig_id = migration['id']
                file_path = migration['file_path']
                
                # Check if migration file exists
                if not os.path.exists(file_path):
                    error_msg = f"Migration file not found: {file_path}"
                    logger.error(error_msg)
                    raise FileNotFoundError(error_msg)
                
                current_checksum = self.calculate_checksum(file_path)
                
                # Check if migration was already executed
                if mig_id in executed_migrations:
                    executed_mig = executed_migrations[mig_id]
                    
                    # Verify checksum to detect changes
                    if executed_mig.checksum != current_checksum:
                        error_msg = (
                            f"Migration {mig_id} has been modified after execution. "
                            f"Database is in inconsistent state."
                        )
                        logger.error(error_msg)
                        raise RuntimeError(error_msg)
                    
                    logger.info(f"Migration {mig_id} already executed, skipping")
                    continue
                
                # Execute new migration
                logger.info(f"Executing migration {mig_id}: {file_path}")
                self.execute_migration(file_path)
                
                # Log migration execution
                migration_log = MigrationLog(
                    migration_id=mig_id,
                    file_path=file_path,
                    checksum=current_checksum
                )
                db.session.add(migration_log)
                db.session.commit()
                
                logger.info(f"Successfully completed migration {mig_id}")
            
            logger.info("Migration process completed successfully")
            
        except Exception as e:
            logger.error(f"Migration process failed: {str(e)}")
            raise

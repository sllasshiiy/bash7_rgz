import yaml
import os
import hashlib
import logging
from sqlalchemy import text

class Migrator:
    def __init__(self, db):
        self.db = db
        self.logger = logging.getLogger(__name__)

    def create_migrations_log_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS migrations_log (
            id SERIAL PRIMARY KEY,
            migration_id INTEGER NOT NULL UNIQUE,
            file_path VARCHAR(500) NOT NULL,
            executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            checksum VARCHAR(64) NOT NULL
        );'''
        
        try:
            self.db.session.execute(text(sql))
            self.db.session.commit()
            self.logger.info("Таблица migrations_log создана успешно")
            return True
        except Exception as e:
            self.logger.error(f"Ошибка при создании таблицы: {e}")
            return False

    def load_changelog(self):
        """Загрузка changelog.yaml"""
        try:
            with open('changelog.yaml', 'r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            self.logger.error(f"Ошибка загрузки changelog: {e}")
            return []

    def calculate_checksum(self, file_path):
        """Вычисление контрольной суммы файла"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                return hashlib.sha256(content.encode()).hexdigest()
        except Exception as e:
            self.logger.error(f"Ошибка вычисления checksum для {file_path}: {e}")
            return None

    def get_executed_migrations(self):
        """Получение выполненных миграций из БД"""
        try:
            result = self.db.session.execute(
                text("SELECT migration_id, file_path, checksum FROM migrations_log")
            )
            return {row[0]: {'file_path': row[1], 'checksum': row[2]} for row in result}
        except Exception as e:
            self.logger.error(f"Ошибка получения выполненных миграций: {e}")
            return {}

    def execute_migration(self, file_path):
        """Выполнение SQL миграции"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                sql_content = file.read()
            
            # Разделяем SQL команды
            statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
            
            for statement in statements:
                if statement:
                    self.db.session.execute(text(statement))
            
            self.db.session.commit()
            self.logger.info(f"Миграция выполнена: {file_path}")
            return True
            
        except Exception as e:
            self.db.session.rollback()
            self.logger.error(f"Ошибка выполнения миграции {file_path}: {e}")
            return False

    def run_migrations(self):
        """Основной метод запуска миграций"""
        self.logger.info("Запуск процесса миграций...")
        
        # Создаем таблицу для лога миграций
        if not self.create_migrations_log_table():
            return False

        # Загружаем changelog
        changelog = self.load_changelog()
        if not changelog:
            self.logger.error("Не удалось загрузить changelog.yaml")
            return False

        # Получаем уже выполненные миграции
        executed_migrations = self.get_executed_migrations()

        for migration in changelog:
            mig_id = migration['id']
            file_path = migration['file_path']

            # Проверяем существование файла миграции
            if not os.path.exists(file_path):
                self.logger.error(f"Файл миграции не найден: {file_path}")
                return False

            current_checksum = self.calculate_checksum(file_path)

            # Проверяем, была ли миграция уже выполнена
            if mig_id in executed_migrations:
                executed_mig = executed_migrations[mig_id]
                
                # Проверяем контрольную сумму
                if executed_mig['checksum'] != current_checksum:
                    self.logger.error(
                        f"Миграция {mig_id} была изменена после выполнения. "
                        f"База данных в несогласованном состоянии."
                    )
                    return False
                
                self.logger.info(f"Миграция {mig_id} уже выполнена, пропускаем")
                continue

            # Выполняем новую миграцию
            self.logger.info(f"Выполнение миграции {mig_id}: {file_path}")
            
            if not self.execute_migration(file_path):
                return False

            # Логируем выполнение миграции
            try:
                self.db.session.execute(
                    text("""
                        INSERT INTO migrations_log (migration_id, file_path, checksum) 
                        VALUES (:migration_id, :file_path, :checksum)
                    """),
                    {
                        'migration_id': mig_id,
                        'file_path': file_path,
                        'checksum': current_checksum
                    }
                )
                self.db.session.commit()
                self.logger.info(f"Миграция {mig_id} успешно завершена")
                
            except Exception as e:
                self.logger.error(f"Ошибка логирования миграции {mig_id}: {e}")
                return False

        self.logger.info("Процесс миграций завершен успешно")
        return True
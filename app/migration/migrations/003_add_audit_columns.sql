-- Добавление поля description к подпискам (пример дополнительной миграции)
ALTER TABLE subscriptions ADD COLUMN IF NOT EXISTS description TEXT;

-- Создание индекса для next_billing_date
CREATE INDEX IF NOT EXISTS idx_subscriptions_next_billing ON subscriptions(next_billing_date);
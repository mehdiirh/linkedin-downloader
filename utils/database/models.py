from utils.database.core import Model


class User(Model):

    table_name = 'users'

    def _create_table(self):
        self.database.execute(
            f"CREATE TABLE IF NOT EXISTS {self.table_name}"
            "("
            "   id BIGINT AUTO_INCREMENT PRIMARY KEY,"
            "   telegram_id INT(16) NOT NULL,"
            "   linkedin_id VARCHAR(256) CHARSET utf8mb4 NULL,"
            "   language VARCHAR(2) NULL,"
            "   date_joined DATETIME DEFAULT CURRENT_TIMESTAMP() NULL,"
            "   last_activity DATETIME NULL,"
            "   CONSTRAINT linkedin_id UNIQUE (linkedin_id),"
            "   CONSTRAINT telegram_id UNIQUE (telegram_id)"
            ")"
        )

    def language(self, telegram_id):
        """
        Get user selected language

        Args:
            telegram_id: user telegram ID

        Returns:
            (str): user language code or None if not selected
        """

        lang = self.database.fetch(
            f"SELECT language FROM users WHERE telegram_id={telegram_id}", size=1
        )
        if lang:
            return lang[0]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.database.close()

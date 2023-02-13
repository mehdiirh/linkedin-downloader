from utils.database.core import Model


class User(Model):

    table_name = "users"

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

        lang = self.fetch(columns="language", telegram_id=telegram_id, size=1)
        if lang:
            return lang[0]


class Media(Model):

    table_name = "media"

    def _create_table(self):
        self.database.execute(
            f"CREATE TABLE IF NOT EXISTS {self.table_name} "
            "("
            "   id BIGINT NOT NULL AUTO_INCREMENT,"
            "   dnr BIGINT NOT NULL,"
            "   user_tg_id INT(16) NOT NULL,"
            "   media_type VARCHAR(16) NOT NULL,"
            "   media_count INT NOT NULL,"
            "   link TEXT NULL,"
            "   error_on_send BOOL NOT NULL DEFAULT FALSE,"
            "   error_type VARCHAR(128) NULL,"
            "   create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,"
            "   PRIMARY KEY (id),"
            "   INDEX (dnr),"
            "   INDEX (user_tg_id),"
            "   INDEX (media_type),"
            "   FOREIGN KEY (dnr) REFERENCES download_requests(id) ON DELETE CASCADE,"
            "   FOREIGN KEY (user_tg_id) REFERENCES users(telegram_id) ON DELETE CASCADE"
            ")"
        )

        return True


class DownloadRequest(Model):

    table_name = "download_requests"

    def _create_table(self):
        self.database.execute(
            f"CREATE TABLE IF NOT EXISTS {self.table_name} "
            f"("
            f"  id BIGINT NOT NULL AUTO_INCREMENT,"
            f"  user_tg_id INT(16) NOT NULL,"
            f"  create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,"
            f"  PRIMARY KEY (id),"
            f"  INDEX (user_tg_id),"
            f"  FOREIGN KEY (user_tg_id) "
            f"  REFERENCES users(telegram_id) ON DELETE CASCADE"
            f")"
        )

import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailClient:
    def __init__(self, smtp_server, imap_server, login, password):
        """
        Инициализация клиента для работы с электронной почтой.

        :param smtp_server: Адрес SMTP сервера.
        :param imap_server: Адрес IMAP сервера.
        :param login: Логин пользователя.
        :param password: Пароль пользователя.
        """
        self.smtp_server = smtp_server
        self.imap_server = imap_server
        self.login = login
        self.password = password

    def send_email(self, subject, recipients, message):
        """
        Отправка письма через SMTP сервер.

        :param subject: Тема письма.
        :param recipients: Список адресатов.
        :param message: Текст сообщения.
        """
        # Создание сообщения в формате MIME
        msg = MIMEMultipart()
        msg['From'] = self.login
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = subject
        msg.attach(MIMEText(message))

        # Подключение к SMTP серверу и отправка письма
        with smtplib.SMTP(self.smtp_server, 587) as server:
            server.ehlo()  # Идентификация клиента
            server.starttls()  # Шифрование соединения TLS
            server.ehlo()  # Повторная идентификация после шифрования
            server.login(self.login, self.password)  # Авторизация
            server.sendmail(self.login, recipients, msg.as_string())  # Отправка письма

    def receive_email(self, header=None):
        """
        Получение письма из IMAP сервера по заголовку.

        :param header: Заголовок письма для фильтрации. Если None, будут выбраны все письма.
        :return: Объект email.message с содержимым письма.
        """
        # Подключение к IMAP серверу и выбор папки "Входящие"
        with imaplib.IMAP4_SSL(self.imap_server) as mail:
            mail.login(self.login, self.password)  # Авторизация
            mail.select("inbox")  # Выбор папки "Входящие"
            # Поиск писем по заданному критерию
            criterion = f'(HEADER Subject "{header}")' if header else 'ALL'
            result, data = mail.uid('search', None, criterion)  # Поиск писем по UID
            assert data[0], 'There are no letters with current header'  # Проверка на наличие писем
            latest_email_uid = data[0].split()[-1]  # Получение UID последнего письма
            result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')  # Извлечение содержимого письма
            raw_email = data[0][1]
            email_message = email.message_from_string(raw_email)  # Парсинг письма в формат email.message
            return email_message  # Возврат объекта email.message


if __name__ == '__main__':
    # Константы для подключения к серверам
    GMAIL_SMTP = "smtp.gmail.com"
    GMAIL_IMAP = "imap.gmail.com"
    login = 'login@gmail.com'  # Логин пользователя
    password = 'qwerty'  # Пароль пользователя

    # Создание экземпляра клиента для работы с почтой
    email_client = EmailClient(GMAIL_SMTP, GMAIL_IMAP, login, password)

    # Отправка письма
    subject = 'Subject'  # Тема письма
    recipients = ['vasya@email.com', 'petya@email.com']  # Список получателей
    message = 'Message'  # Текст сообщения
    email_client.send_email(subject, recipients, message)  # Вызов метода отправки письма

    # Получение письма
    header = None  # Заголовок для фильтрации (можно изменить)
    email_message = email_client.receive_email(header)  # Вызов метода получения письма
    print(email_message)  # Вывод содержимого письма

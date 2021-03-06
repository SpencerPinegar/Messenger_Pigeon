from Messenger_Pigeon.Objects.ksl_scraper import KSL_SCRAPER
from Messenger_Pigeon.Objects.Database_Objects.database_error import ScraperException
import os

required_keys = ['Range', 'Number_To_Notify',
                 'Max_Pages', 'Proxy_IP',
                 'DB_Host', 'DB_User',
                 'DB_Password', 'DB_Name',
                 'Email_Server', 'Email_To_Notify',
                 'Email_To_Send', 'Email_Password']


def main():
    settings = get_settings()
    _range = settings['Range']
    number_to_notify = format_settings_array(settings['Number_To_Notify'])
    proxy_ip = settings['Proxy_IP']
    db_host = settings['DB_Host']
    db_user = settings['DB_User']
    db_password = settings['DB_Password']
    db_name = settings['DB_Name']
    max_pages = int(settings['Max_Pages'])

    email_to_send = settings['Email_To_Send']
    email_password = settings['Email_Password']
    email_server = settings['Email_Server']
    emails_to_notify = format_settings_array(settings['Email_To_Notify'])

    directory = os.path.dirname(__file__)

    the_scraper = KSL_SCRAPER(_range=_range,
                              number_to_notify=number_to_notify,
                              email_to_send=email_to_send,
                              email_password=email_password,
                              email_service=email_server,
                              email_to_recieve=emails_to_notify,
                              proxy_ip=proxy_ip,
                              db_host=db_host,
                              db_user=db_user,
                              db_password=db_password,
                              db_name=db_name,
                              logs_file_path=directory
                              )
    while True:
        try:
            the_scraper.work(max_pages)
        except Exception as e:
            print(str(e))
            new_error = ScraperException(e, 'Main level exception', ScraperException)
            try:
                the_scraper.data_base.add_object(new_error)
                the_scraper = KSL_SCRAPER(_range=_range,
                                          number_to_notify=number_to_notify,
                                          email_to_send=email_to_send,
                                          email_password=email_password,
                                          email_service=email_server,
                                          email_to_recieve=emails_to_notify,
                                          proxy_ip=proxy_ip,
                                          db_host=db_host,
                                          db_user=db_user,
                                          db_password=db_password,
                                          db_name=db_name,
                                          logs_file_path=directory
                                          )
            except Exception as e:
                the_scraper.texter.send_message(the_scraper.to_number, "THE SCRAPER IS SHUTTING DOWN!!!! "
                                                                       f"Cause:: {str(e)}")
                exit(-1)


def get_settings():
    """
    Reads the settings file and
    :return:
    """
    settings = {}
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, 'SETTINGS')
    try:
        with open(filename) as settings_file:
            for line in settings_file.readlines():
                if line.__contains__('::'):
                    key_value = line.split('::')
                    key = key_value[0]
                    value = key_value[1].split("'")[1]
                    settings[key] = value
        for key in required_keys:
            if not settings.keys().__contains__(key):
                raise Exception()
        return settings
    except Exception as e:
        raise Exception("There was an issue reading the SETTINGS.txt file.")


def format_settings_array(array_string: str):
    """
    Formats a string representation of numbers to an array of numbers
    :param array_string: The array of numbers expressed as a string
    :return: The numbers from string as sn array of numbers in strings
    """
    array_string = array_string.split(',')
    number_array = []
    for number in array_string:
        number = number.strip().strip("'")
        number_array.append(number)
    return number_array


if __name__ == '__main__':
    main()

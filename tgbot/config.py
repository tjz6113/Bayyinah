import sqlite3
from dataclasses import dataclass
from typing import Optional

from environs import Env

paths_dict_rev = {"New to Arabic": "01", "Understand Arabic": "02", "10 Days Challenge": "0101",
                  "Reading Fluency": "0102", "The Basics": "0201", "The Basics and Beyond": "0202", "Unit 1": "020101",
                  "Unit 2": "020102", "Unit 3": "020103", "Unit 4": "020104", "Unit 5": "020105", "Unit 6": "020106",
                  "Unit 7": "020107", "Unit 8": "020108", "Unit 9": "020109", "Unit 10": "020110", "Unit 11": "020111",
                  "Unit 12": "020112", "Unit 13": "020113", "Unit 14": "020114", "Unit 15": "020115", "Dream": "020201",
                  "Reading The Classics": "020202", "Basic Nahw": "02020101", "Basic Sarf": "02020102", "Advanced Sarf": "02020103",
                  "Advanced Nahw & Structures": "02020104", "Balagha": "02020105", "Baqarah Beyond Translation": "02020106",
                  "Dream BIG 2023": "02020107"}



kb_dict = {'00': ['01', '02'],
           '01': ['0101', '0102'],
           '02': ['0201', '0202'],
           '0101': ['010101', '010102'],
           '0102': ['010201', '010202'],
           '010201': ['01020101', '01020102', '01020103', '01020104', '01020105', '01020106', '01020107', '01020108',
                      '01020109', '01020110', '01020111', '01020112', '01020113', '01020114', '01020115'],
           '010202': ['01020201', '01020202'],
           '01020201': ['0102020101', '0102020102', '0102020103', '0102020104', '0102020105', '0102020106',
                        '0102020107'],
           '0201': ['02010', '020102', '020103', '020104', '020105', '020106', '020107', '020108', '020109', '020110',
                    '020111', '020112', '020113', '020114', '020115', '020116', '020117', '020118', '020119', '020120',
                    '020121', '020122', '020123'],
           '0202': ['020201', '020202'],
           '020201': ['020201001', '020201002', '020201003', '020201004', '020201005', '020201006', '020201007',
                      '020201008', '020201009', '020201010', '020201011', '020201012', '020201013', '020201014',
                      '020201015', '020201016', '020201017', '020201018', '020201019', '020201020', '020201021',
                      '020201022', '020201023', '020201024', '020201025', '020201026', '020201027', '020201028',
                      '020201029', '020201030', '020201031', '020201032', '020201033', '020201034', '020201035',
                      '020201036', '020201037', '020201038', '020201039', '020201040', '020201041', '020201042',
                      '020201043', '020201044', '020201045', '020201046', '020201047', '020201048', '020201049',
                      '020201050', '020201051', '020201052', '020201053', '020201054', '020201055', '020201056',
                      '020201057', '020201058', '020201059', '020201060', '020201061', '020201062', '020201063',
                      '020201064', '020201065', '020201066', '020201067', '020201068', '020201069', '020201070',
                      '020201071', '020201072', '020201073', '020201074', '020201075', '020201076', '020201077',
                      '020201078', '020201079', '020201080', '020201081', '020201082', '020201083', '020201084',
                      '020201085', '020201086', '020201087', '020201088', '020201089', '020201090', '020201091',
                      '020201092', '020201093', '020201094', '020201095', '020201096', '020201097', '020201098',
                      '020201099', '020201100', '020201101', '020201102', '020201103', '020201104', '020201105',
                      '020201106', '020201107', '020201108', '020201109', '020201110', '020201111', '020201112',
                      '020201113', '020201114'],
           '020202': ['020202001', '020202002', '020202003', '020202004', '020202005', '020202006', '020202007',
                      '020202008', '020202009', '020202010', '020202011', '020202012', '020202013', '020202014',
                      '020202015', '020202016', '020202017', '020202018', '020202019', '020202020', '020202021',
                      '020202022', '020202023', '020202024', '020202025', '020202026', '020202027', '020202028',
                      '020202029', '020202030', '020202031', '020202032', '020202033', '020202034', '020202035',
                      '020202036', '020202037', '020202038', '020202039', '020202040', '020202041', '020202042',
                      '020202043', '020202044', '020202045', '020202046', '020202047', '020202048', '020202049',
                      '020202050', '020202051', '020202052', '020202053', '020202054', '020202055', '020202056',
                      '020202057', '020202058', '020202059', '020202060', '020202061', '020202062', '020202063',
                      '020202064', '020202065', '020202066', '020202067', '020202068', '020202069', '020202070',
                      '020202071', '020202072', '020202073', '020202074', '020202075', '020202076', '020202077',
                      '020202078', '020202079', '020202080', '020202081', '020202082', '020202083', '020202084',
                      '020202085', '020202086', '020202087', '020202088', '020202089', '020202090', '020202091',
                      '020202092', '020202093', '020202094', '020202095', '020202096', '020202097', '020202098',
                      '020202099', '020202100', '020202101', '020202102', '020202103', '020202104', '020202105',
                      '020202106', '020202107', '020202108', '020202109', '020202110', '020202111', '020202112',
                      '020202113', '020202114']}

paths_dict = {"01": "Arabic",
              "02": "Quran",
              "0101": "New to Arabic",
              "0102": "Understand Arabic",
              "010101": "10 Days Challenge",
              "010102": "Reading Fluency",
              "010201": "The Basics",
              "010202": "The Basics and Beyond",
              "01020101": "Unit 1",
              "01020102": "Unit 2",
              "01020103": "Unit 3",
              "01020104": "Unit 4",
              "01020105": "Unit 5",
              "01020106": "Unit 6",
              "01020107": "Unit 7",
              "01020108": "Unit 8",
              "01020109": "Unit 9",
              "01020110": "Unit 10",
              "01020111": "Unit 11",
              "01020112": "Unit 12",
              "01020113": "Unit 13",
              "01020114": "Unit 14",
              "01020115": "Unit 15",
              "01020201": "Dream",
              "01020202": "Reading The Classics",
              "0102020101": "Basic Nahw",
              "0102020102": "Basic Sarf",
              "0102020103": "Advanced Sarf",
              "0102020104": "Advanced Nahw & Structures",
              "0102020105": "Balagha",
              "0102020106": "Baqarah Beyond Translation",
              "0102020107": "Dream BIG 2023",
              "0201": "Courses",
              "0202": "Surahs",
              "02010": 'Hikmah In The Quran',
              "020102": 'Divine Speech',
              "020103": 'Story Nights',
              "020104": 'Parenting',
              "020105": 'How To Pray (Story Of Prayer)',
              "020106": 'Hijab',
              "020107": 'Shame',
              "020108": 'Leadership',
              "020109": 'Four Guided Steps',
              "020110": 'Foundation Of Faith',
              "020111": 'Honoring The Messenger',
              "020112": 'The Journey Of Faith',
              "020113": 'A Thematic Overview',
              "020114": 'Heavenly Order',
              "020115": 'Reading The Quran With Your Heart',
              "020116": 'Virtues of Laylat Al-Qadr',
              "020117": 'History - The Four Imams',
              "020118": 'History - Masjid Al-Aqsa',
              "020119": 'History - The Five Abdullahs',
              "020120": 'History - Abu Huraira',
              "020121": 'History - Mothers Of The Believers',
              "020122": 'History - Black and Noble',
              "020123": 'Quran Aur Hum (Quran & Us)',
              "020201": "Concise commentary",
              "020202": "Deeper look",
              '020201001': '1. Al-Fatihah',
              '020201002': '2. Al-Baqarah',
              '020201003': '3. Ali `Imran',
              '020201004': '4. An-Nisa',
              '020201005': '5. Al-Maidah',
              '020201006': '6. Al-An`am',
              '020201007': '7. Al-A`raf',
              '020201008': '8. Al-Anfal',
              '020201009': '9. At-Tawbah',
              '020201010': '10. Yunus',
              '020201011': '11. Hud',
              '020201012': '12. Yusuf',
              '020201013': '13. Ar-Ra`d',
              '020201014': '14. Ibrahim',
              '020201015': '15. Al-Hijr',
              '020201016': '16. An-Nahl',
              '020201017': '17. Al-Isra',
              '020201018': '18. Al-Kahf',
              '020201019': '19. Maryam',
              '020201020': '20. Taha',
              '020201021': '21. Al-Anbya',
              '020201022': '22. Al-Hajj',
              '020201023': '23. Al-Mu`minun',
              '020201024': '24. An-Nur',
              '020201025': '25. Al-Furqan',
              '020201026': '26. Ash-Shu`ara',
              '020201027': '27. An-Naml',
              '020201028': '28. Al-Qasas',
              '020201029': '29. Al-`Ankabut',
              '020201030': '30. Ar-Rum',
              '020201031': '31. Luqman',
              '020201032': '32. As-Sajdah',
              '020201033': '33. Al-Ahzab',
              '020201034': '34. Saba',
              '020201035': '35. Fatir',
              '020201036': '36. Ya-Sin',
              '020201037': '37. As-Saffat',
              '020201038': '38. Sad',
              '020201039': '39. Az-Zumar',
              '020201040': '40. Ghafir',
              '020201041': '41. Fussilat',
              '020201042': '42. Ash-Shuraa',
              '020201043': '43. Az-Zukhruf',
              '020201044': '44. Ad-Dukhan',
              '020201045': '45. Al-Jathiyah',
              '020201046': '46. Al-Ahqaf',
              '020201047': '47. Muhammad',
              '020201048': '48. Al-Fath',
              '020201049': '49. Al-Hujurat',
              '020201050': '50. Qaf',
              '020201051': '51. Adh-Dhariyat',
              '020201052': '52. At-Tur',
              '020201053': '53. An-Najm',
              '020201054': '54. Al-Qamar',
              '020201055': '55. Ar-Rahman',
              '020201056': '56. Al-Waqi`ah',
              '020201057': '57. Al-Hadid',
              '020201058': '58. Al-Mujadila',
              '020201059': '59. Al-Hashr',
              '020201060': '60. Al-Mumtahanah',
              '020201061': '61. As-Saf',
              '020201062': '62. Al-Jumu`ah',
              '020201063': '63. Al-Munafiqun',
              '020201064': '64. At-Taghabun',
              '020201065': '65. At-Talaq',
              '020201066': '66. At-Tahrim',
              '020201067': '67. Al-Mulk',
              '020201068': '68. Al-Qalam',
              '020201069': '69. Al-Haqqah',
              '020201070': '70. Al-Ma`arij',
              '020201071': '71. Nuh',
              '020201072': '72. Al-Jinn',
              '020201073': '73. Al-Muzzammil',
              '020201074': '74. Al-Muddaththir',
              '020201075': '75. Al-Qiyamah',
              '020201076': '76. Al-Insan',
              '020201077': '77. Al-Mursalat',
              '020201078': '78. An-Naba',
              '020201079': '79. An-Nazi`at',
              '020201080': '80. `Abasa',
              '020201081': '81. At-Takwir',
              '020201082': '82. Al-Infitar',
              '020201083': '83. Al-Mutaffifin',
              '020201084': '84. Al-Inshiqaq',
              '020201085': '85. Al-Buruj',
              '020201086': '86. At-Tariq',
              '020201087': '87. Al-A`la',
              '020201088': '88. Al-Ghashiyah',
              '020201089': '89. Al-Fajr',
              '020201090': '90. Al-Balad',
              '020201091': '91. Ash-Shams',
              '020201092': '92. Al-Layl',
              '020201093': '93. Ad-Duhaa',
              '020201094': '94. Ash-Sharh',
              '020201095': '95. At-Tin',
              '020201096': '96. Al-`Alaq',
              '020201097': '97. Al-Qadr',
              '020201098': '98. Al-Bayyinah',
              '020201099': '99. Az-Zalzalah',
              '020201100': '100. Al-`Adiyat',
              '020201101': '101. Al-Qari`ah',
              '020201102': '102. At-Takathur',
              '020201103': '103. Al-`Asr',
              '020201104': '104. Al-Humazah',
              '020201105': '105. Al-Fil',
              '020201106': '106. Quraysh',
              '020201107': '107. Al-Ma`un',
              '020201108': '108. Al-Kawthar',
              '020201109': '109. Al-Kafirun',
              '020201110': '110. An-Nasr',
              '020201111': '111. Al-Masad',
              '020201112': '112. Al-Ikhlas',
              '020201113': '113. Al-Falaq',
              '020201114': '114. An-Nas',
              '020202001': '1. Al-Fatihah',
              '020202002': '2. Al-Baqarah',
              '020202003': '3. Ali `Imran',
              '020202004': '4. An-Nisa',
              '020202005': '5. Al-Maidah',
              '020202006': '6. Al-An`am',
              '020202007': '7. Al-A`raf',
              '020202008': '8. Al-Anfal',
              '020202009': '9. At-Tawbah',
              '020202010': '10. Yunus',
              '020202011': '11. Hud',
              '020202012': '12. Yusuf',
              '020202013': '13. Ar-Ra`d',
              '020202014': '14. Ibrahim',
              '020202015': '15. Al-Hijr',
              '020202016': '16. An-Nahl',
              '020202017': '17. Al-Isra',
              '020202018': '18. Al-Kahf',
              '020202019': '19. Maryam',
              '020202020': '20. Taha',
              '020202021': '21. Al-Anbya',
              '020202022': '22. Al-Hajj',
              '020202023': '23. Al-Mu`minun',
              '020202024': '24. An-Nur',
              '020202025': '25. Al-Furqan',
              '020202026': '26. Ash-Shu`ara',
              '020202027': '27. An-Naml',
              '020202028': '28. Al-Qasas',
              '020202029': '29. Al-`Ankabut',
              '020202030': '30. Ar-Rum',
              '020202031': '31. Luqman',
              '020202032': '32. As-Sajdah',
              '020202033': '33. Al-Ahzab',
              '020202034': '34. Saba',
              '020202035': '35. Fatir',
              '020202036': '36. Ya-Sin',
              '020202037': '37. As-Saffat',
              '020202038': '38. Sad',
              '020202039': '39. Az-Zumar',
              '020202040': '40. Ghafir',
              '020202041': '41. Fussilat',
              '020202042': '42. Ash-Shuraa',
              '020202043': '43. Az-Zukhruf',
              '020202044': '44. Ad-Dukhan',
              '020202045': '45. Al-Jathiyah',
              '020202046': '46. Al-Ahqaf',
              '020202047': '47. Muhammad',
              '020202048': '48. Al-Fath',
              '020202049': '49. Al-Hujurat',
              '020202050': '50. Qaf',
              '020202051': '51. Adh-Dhariyat',
              '020202052': '52. At-Tur',
              '020202053': '53. An-Najm',
              '020202054': '54. Al-Qamar',
              '020202055': '55. Ar-Rahman',
              '020202056': '56. Al-Waqi`ah',
              '020202057': '57. Al-Hadid',
              '020202058': '58. Al-Mujadila',
              '020202059': '59. Al-Hashr',
              '020202060': '60. Al-Mumtahanah',
              '020202061': '61. As-Saf',
              '020202062': '62. Al-Jumu`ah',
              '020202063': '63. Al-Munafiqun',
              '020202064': '64. At-Taghabun',
              '020202065': '65. At-Talaq',
              '020202066': '66. At-Tahrim',
              '020202067': '67. Al-Mulk',
              '020202068': '68. Al-Qalam',
              '020202069': '69. Al-Haqqah',
              '020202070': '70. Al-Ma`arij',
              '020202071': '71. Nuh',
              '020202072': '72. Al-Jinn',
              '020202073': '73. Al-Muzzammil',
              '020202074': '74. Al-Muddaththir',
              '020202075': '75. Al-Qiyamah',
              '020202076': '76. Al-Insan',
              '020202077': '77. Al-Mursalat',
              '020202078': '78. An-Naba',
              '020202079': '79. An-Nazi`at',
              '020202080': '80. `Abasa',
              '020202081': '81. At-Takwir',
              '020202082': '82. Al-Infitar',
              '020202083': '83. Al-Mutaffifin',
              '020202084': '84. Al-Inshiqaq',
              '020202085': '85. Al-Buruj',
              '020202086': '86. At-Tariq',
              '020202087': '87. Al-A`la',
              '020202088': '88. Al-Ghashiyah',
              '020202089': '89. Al-Fajr',
              '020202090': '90. Al-Balad',
              '020202091': '91. Ash-Shams',
              '020202092': '92. Al-Layl',
              '020202093': '93. Ad-Duhaa',
              '020202094': '94. Ash-Sharh',
              '020202095': '95. At-Tin',
              '020202096': '96. Al-`Alaq',
              '020202097': '97. Al-Qadr',
              '020202098': '98. Al-Bayyinah',
              '020202099': '99. Az-Zalzalah',
              '020202100': '100. Al-`Adiyat',
              '020202101': '101. Al-Qari`ah',
              '020202102': '102. At-Takathur',
              '020202103': '103. Al-`Asr',
              '020202104': '104. Al-Humazah',
              '020202105': '105. Al-Fil',
              '020202106': '106. Quraysh',
              '020202107': '107. Al-Ma`un',
              '020202108': '108. Al-Kawthar',
              '020202109': '109. Al-Kafirun',
              '020202110': '110. An-Nasr',
              '020202111': '111. Al-Masad',
              '020202112': '112. Al-Ikhlas',
              '020202113': '113. Al-Falaq',
              '020202114': '114. An-Nas'
              }


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_videos(self):
        sql = """
CREATE TABLE IF NOT EXISTS 'video'(
	"id"	VARCHAR NOT NULL,
	"folder"	VARCHAR NOT NULL,
	"video"	VARCHAR NOT NULL,
	"filename"	VARCHAR(300) NOT NULL,
	"fileID"	VARCHAR(300) NOT NULL,
	PRIMARY KEY('id')
);
"""
        self.execute(sql, commit=True)

    def create_table_files(self):
        sql = """
CREATE TABLE IF NOT EXISTS 'file'(
  id VARCHAR NOT NULL PRIMARY KEY,
  video VARCHAR NOT NULL,
  filename VARCHAR(300) NOT NULL,
  fileID VARCHAR(300) NOT NULL,
  FOREIGN KEY (video) REFERENCES 'video'(video)
);
"""
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([f"{item} = ?" for item in parameters])
        return sql, tuple(parameters.values())

    def add_video(self, id: str, folder: str, video: str, filename: str, fileID: str):
        sql = """
        INSERT INTO video( id, folder, video, filename, fileID) VALUES(?, ?, ?, ?, ?)
        """
        self.execute(sql, parameters=(
            id, folder, video, filename, fileID), commit=True)

    def add_file(self, id: str, video: str, filename: str, fileID: str):
        sql = """
        INSERT INTO file(id, video, filename, fileID) VALUES(?, ?, ?, ?)
        """
        print(sql)
        self.execute(sql, parameters=(
            id, video, filename, fileID), commit=True)

    def select_all_videos_from_folder(self, folder):
        sql = """
        SELECT * FROM video WHERE folder={folder}
        """.format(folder=folder)
        return self.execute(sql, fetchall=True)

    def select_all_files_from_folder(self, folder):
        sql = """
        SELECT * FROM file WHERE folder={folder}
        """.format(folder=folder)
        return self.execute(sql, fetchall=True)

    def select_videos(self, **kwargs):
        sql = "SELECT fileID, filename FROM video WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchall=True)

    def select_videos_for_kb(self, **kwargs):
        sql2 = 'ORDER BY id'
        sql = "SELECT id, filename FROM video WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        sql = sql +' '+ sql2
        return self.execute(sql, parameters=parameters, fetchall=True)

    def select_files(self, **kwargs):
        sql2 = 'ORDER BY id'
        sql = f"SELECT filename, fileID FROM file WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        sql = sql +' '+ sql2
        return self.execute(sql, parameters=parameters, fetchall=True)

    def count_videos(self, **kwargs):
        sql = f"SELECT COUNT (*) FROM video WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_files(self, **kwargs):
        sql = f"SELECT COUNT (*) FROM video WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def delete(self, type, kwargs):
        # True if video
        if type:
            sql = f"DELETE * FROM video WHERE "
        else:
            sql = f"DELETE * FROM file WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)


db = Database(path_to_db='main.db')


def logger(statement):
    print(f"""
_____________________________________________________
Executing:
{statement}
_____________________________________________________
""")


@dataclass
class DbConfig:
    """
    Database configuration class.
    This class holds the settings for the database, such as host, password, port, etc.

    Attributes
    ----------
    host : str
        The host where the database server is located.
    password : str
        The password used to authenticate with the database.
    user : str
        The username used to authenticate with the database.
    database : str
        The name of the database.
    port : int
        The port where the database server is listening.
    """

    host: str
    password: str
    user: str
    database: str
    port: int = 5432

    # For SQLAlchemy
    def construct_sqlalchemy_url(self, driver="asyncpg", host=None, port=None) -> str:
        """
        Constructs and returns a SQLAlchemy URL for this database configuration.
        """

        from sqlalchemy.engine.url import URL

        if not host:
            host = self.host
        if not port:
            port = self.port
        uri = URL.create(drivername=f"postgresql+{driver}", username=self.user, password=self.password, host=host,
                         port=port, database=self.database, )
        return uri.render_as_string(hide_password=False)

    @staticmethod
    def from_env(env: Env):
        """
        Creates the DbConfig object from environment variables.
        """
        host = env.str("DB_HOST")
        password = env.str("POSTGRES_PASSWORD")
        user = env.str("POSTGRES_USER")
        database = env.str("POSTGRES_DB")
        port = env.int("DB_PORT", 5432)
        return DbConfig(host=host, password=password, user=user, database=database, port=port)


@dataclass
class TgBot:
    """
    Creates the TgBot object from environment variables.
    """

    token: str
    admin_ids: list[int]
    use_redis: bool

    @staticmethod
    def from_env(env: Env):
        """
        Creates the TgBot object from environment variables.
        """
        token = env.str("BOT_TOKEN")
        admin_ids = list(map(int, env.list("ADMINS")))
        use_redis = env.bool("USE_REDIS")
        return TgBot(token=token, admin_ids=admin_ids, use_redis=use_redis)


@dataclass
class RedisConfig:
    """
    Redis configuration class.

    Attributes
    ----------
    redis_pass : Optional(str)
        The password used to authenticate with Redis.
    redis_port : Optional(int)
        The port where Redis server is listening.
    redis_host : Optional(str)
        The host where Redis server is located.
    """

    redis_pass: Optional[str]
    redis_port: Optional[int]
    redis_host: Optional[str]

    def dsn(self) -> str:
        """
        Constructs and returns a Redis DSN (Data Source Name) for this database configuration.
        """
        if self.redis_pass:
            return f"redis://:{self.redis_pass}@{self.redis_host}:{self.redis_port}/0"
        else:
            return f"redis://{self.redis_host}:{self.redis_port}/0"

    @staticmethod
    def from_env(env: Env):
        """
        Creates the RedisConfig object from environment variables.
        """
        redis_pass = env.str("REDIS_PASSWORD")
        redis_port = env.int("REDIS_PORT")
        redis_host = env.str("REDIS_HOST")

        return RedisConfig(redis_pass=redis_pass, redis_port=redis_port, redis_host=redis_host)


@dataclass
class Miscellaneous:
    """
    Miscellaneous configuration class.

    This class holds settings for various other parameters.
    It merely serves as a placeholder for settings that are not part of other categories.

    Attributes
    ----------
    other_params : str, optional
        A string used to hold other various parameters as required (default is None).
    """

    other_params: str = None


@dataclass
class Config:
    """
    The main configuration class that integrates all the other configuration classes.

    This class holds the other configuration classes, providing a centralized point of access for all settings.

    Attributes
    ----------
    tg_bot : TgBot
        Holds the settings related to the Telegram Bot.
    misc : Miscellaneous
        Holds the values for miscellaneous settings.
    db : Optional[DbConfig]
        Holds the settings specific to the database (default is None).
    redis : Optional[RedisConfig]
        Holds the settings specific to Redis (default is None).
    """

    tg_bot: TgBot
    misc: Miscellaneous
    db: Optional[DbConfig] = None
    redis: Optional[RedisConfig] = None


def load_config(path: str = None) -> Config:
    """
    This function takes an optional file path as input and returns a Config object.
    :param path: The path of env file from where to load the configuration variables.
    It reads environment variables from a .env file if provided, else from the process environment.
    :return: Config object with attributes set as per environment variables.
    """

    # Create an Env object.
    # The Env object will be used to read environment variables.
    env = Env()
    env.read_env(path)

    return Config(tg_bot=TgBot.from_env(env),  # db=DbConfig.from_env(env),
                  # redis=RedisConfig.from_env(env),
                  misc=Miscellaneous(), )

#!/bin/python

class Temperature:
    def __init__(self):
        from zeus import ZeusSession
        self._session = ZeusSession()

    def save(self):
        VALUE_MIN = 0.0
        VALUE_MAX = 37.5

        value = input('>>> Input your temperature (\'C): ')
        value = float(value)
        if value < VALUE_MIN or value >= VALUE_MAX:
            raise Exception(f'Invalid value: {value}')

        self._session.save(
            pg_key='PERS01^PERS01_09^002^AmcDailyTempRegE',
            temp=value,
            sympt_1=False,
            sympt_2=False,
            sympt_3=False,
            sympt_4=False,
            sympt_5=False,
            sympt_6=False,
            spc_ctnt='',
        )

    def show_task_log(self):
        from datetime import datetime
        print(self._session.select(
            pg_key='PERS01^PERS01_09^003^UsdAsstcrDiaryAplyE',
            posi_univ_clsf_cd='USR01.GRSC',
            asstcr_slt_shtm_cd='USR03.10',
            asstcr_diary_yy=datetime.today().strftime(r'%Y'),
            asstcr_diary_mm='',
            asstcr_diary_sbjt='',
            lang_cd='',
            page_open_time='',
        ))


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()

    Temperature().show_task_log()

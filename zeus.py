from datetime import datetime
import requests


class ZeusSession:
    def __init__(self):
        import os
        self._user_id = os.environ['USER_ID']
        self._user_pw = os.environ['USER_PW']

        self._dept_cd = ''
        self._mbr_no = ''

        self._session = requests.session()
        self._login()

    def _login(self):
        url = 'https://zeus.gist.ac.kr/sys/login/auth.do?callback='
        headers = {
            'Host': 'zeus.gist.ac.kr',
            'Origin': 'https://zeus.gist.ac.kr',
            'Referer': 'https://zeus.gist.ac.kr/sys/main/login.do',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0',
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'DNT': '1',
        }
        payload = {
            'login_id': self._user_id,
            'login_pw': self._user_pw,
        }

        r = self._session.post(url, headers=headers, data=payload)
        assert r.status_code == 200

        # update mbr_no, dept_cd
        content = self._post(
            path='/sys/main/role.do',
            pg_key='',
            pg_nm='',
        )
        self._mbr_no, self._dept_cd, *_ = \
            _get(content, 'GRSC') or _get(content, 'USR01.UNIV')

    def _post(self, path: str, pg_key: str, raw: str = None, **payload):
        url = f'https://zeus.gist.ac.kr' + path
        headers = {
            'Host': 'zeus.gist.ac.kr',
            'Origin': 'https://zeus.gist.ac.kr',
            'Referer': 'https://zeus.gist.ac.kr/index.html',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'text/plain;charset=UTF-8',
            'DNT': '1',
        }

        payload['WMONID'] = str(self._session.cookies['WMONID'])
        payload['pg_key'] = pg_key
        payload['page_open_time'] = ''
        payload['page_open_time_on'] = datetime.now().strftime(
            r'%Y%m%d%H%M%S%f'
        )
        payload = 'SSV:utf-8' + SEP + \
            SEP.join(f'{str(k)}={_convert(v)}' for k,
                     v in payload.items()) + SEP
        if raw is not None:
            payload += raw

        r = self._session.post(url, headers=headers,
                               data=payload.encode('utf-8'))
        assert r.status_code == 200
        return r.content.decode('utf-8')

    def select(self, path: str, pg_key: str, **payload):
        return _get(self._post(
            path=path,
            pg_key=pg_key,
            studt_no=self._mbr_no,
            **payload,
        ), 'N' + SEP2)

    def save(self, path: str, pg_key: str, **payload):
        return self._post(
            path=path,
            pg_key=pg_key,
            chk_dt=datetime.today().strftime(r'%Y-%m-%d'),
            mbr_no=self._mbr_no,
            dept_cd=self._dept_cd,
            **payload,
        )


SEP = ''
SEP2 = ''


def _convert(value) -> str:
    if isinstance(value, bool):
        return 'Y' if value else 'N'
    return str(value)


def _get(content: str, key: str) -> list:
    try:
        return content.split(key)[1].split(SEP)[0].split(SEP2)[1:]
    except:
        return None

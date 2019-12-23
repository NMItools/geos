import time
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from clint.textui import progress


def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    """
    Ponavljanje neuspešnih HTTP zahteva
    """
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def img_download(wmst):
    """
    Preuzimanje PNG slike na osnovu definisanog GeoSWMS objekta
    """
    t0 = time.time()
    try:
        # otvaranje WMS linka
        print('Slanje zahteva za preuzimanjem...')
        r = requests_retry_session().get(
            wmst.url,
            headers=wmst.header,
            stream=True)
        print('Uspešno!', r.status_code)
    except Exception as x:
        print('Neuspeli zahtev :(', x.__class__.__name__)
        return False
    else:
        print(f"Preuzimanje slike {wmst.filename}...")
        with open(wmst.path + wmst.filename + ".png", 'wb') as f:
            total_length = int(r.headers.get('content-length'))
            for chunk in progress.bar(
                                      r.iter_content(chunk_size=1024),
                                      expected_size=(total_length/1024) + 1
                                      ):
                if chunk:
                    f.write(chunk)
                    f.flush()
            print('Preuzimanje gotovo!')
    finally:
        t1 = time.time()
        print('Trajanje:', round(t1 - t0, 2), 'sec')
        return True

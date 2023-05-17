import os
import pandas as pd
import json
from typing import Dict, List, Optional, Union, cast
import requests
from env import token, username

url = "https://api.github.com/search/repositories"

repos = ['nightscout/cgm-remote-monitor',
 'atralice/Curso.Prep.Henry',
 'jquery/jquery',
 'TheOdinProject/javascript-exercises',
 'odoo/odoo',
 'anuraghazra/github-readme-stats',
 'tastejs/todomvc',
 'Binaryify/NeteaseCloudMusicApi',
 'actionsdemos/calculator',
 'RedHatTraining/DO288-apps',
 'Shastel/reverse-int',
 'leonardomso/33-js-concepts',
 'hasura/imad-app',
 'learn-co-curriculum/phase-0-intro-to-js-2-array-lab',
 'angular-ui/bootstrap',
 'learn-co-students/js-from-dom-to-node-bootcamp-prep-000',
 'learn-co-students/javascript-intro-to-functions-lab-bootcamp-prep-000',
 'learn-co-curriculum/phase-0-pac-3-intro-to-functions-lab',
 'freeCodeCamp/boilerplate-npm',
 'learn-co-curriculum/phase-0-pac-3-function-parameters-lab',
 'nolimits4web/swiper',
 'bettiolo/node-echo',
 'vuejs/vuex',
 'mozilla/pdf.js',
 'GoogleChrome/lighthouse',
 'OAI/OpenAPI-Specification',
 'Asabeneh/30-Days-Of-JavaScript',
 'Shastel/reverse-int',
 'sahat/hackathon-starter',
 'leonardomso/33-js-concepts',
 'django/django',
 'scikit-learn/scikit-learn',
 'home-assistant/core',
 'pytorch/pytorch',
 'streamlit/streamlit-example',
 'ageitgey/face_recognition',
 'fighting41love/funNLP',
 'swisskyrepo/PayloadsAllTheThings',
 'yandex-praktikum/backend_test_homework',
 'apache/airflow',
 'matterport/Mask_RCNN',
 'CorentinJ/Real-Time-Voice-Cloning',
 'donnemartin/data-science-ipython-notebooks',
 'wangzheng0822/algo',
 'ccxt/ccxt',
 'faif/python-patterns',
 'encode/django-rest-framework',
 'MorvanZhou/tutorials',
 'facebookresearch/Detectron',
 'saltstack/salt',
 'littlecodersh/ItChat',
 'facebookresearch/fairseq',
 'anasty17/mirror-leech-telegram-bot',
 'phoniex628/jd_maotai_seckill',
 'MorvanZhou/Reinforcement-learning-with-tensorflow',
 'Turonk/character_creation_module',
 'davidsandberg/facenet',
 'openai/baselines',
 'quantopian/zipline',
 'ray-project/ray',
 'facebook/react-native',
 'doocs/advanced-java',
 'yankils/hello-world',
 'netty/netty',
 'kdn251/interviews',
 'Blankj/AndroidUtilCode',
 'google/guava',
 'apolloconfig/apollo',
 'xuxueli/xxl-job',
 'apache/hadoop',
 'xkcoding/spring-boot-demo',
 'apolloconfig/apollo',
 'xuxueli/xxl-job',
 'taylor-training/time-tracker',
 'chanjarster/weixin-java-tools',
 'apache/hadoop',
 'macrozheng/mall-learning',
 'MicrosoftDocs/pipelines-java',
 'forezp/SpringCloudLearning',
 'udacity/ud839_Miwok',
 'wuyouzhuguli/SpringAll',
 'shuzheng/zheng',
 'firebase/quickstart-android',
 'square/retrofit',
 'alibaba/canal',
 'JeffLi1993/springboot-learning-example',
 'apache/zookeeper',
 'alibaba/arthas',
 'udacity/ud851-Exercises',
 'linlinjava/litemall',
 'pjreddie/darknet',
 'FFmpeg/FFmpeg',
 'openwrt/openwrt',
 'nothings/stb',
 'obsproject/obs-studio',
 'netdata/netdata',
 'Klipper3d/klipper',
 'arendst/Tasmota',
 'huangz1990/redis-3.0-annotated',
 'gcc-mirror/gcc',
 'ofZach/devart-template',
 'tmux/tmux',
 'RIOT-OS/RIOT',
 'cbuchner1/ccminer',
 'raspberrypi/firmware',
 'analogdevicesinc/no-OS',
 'devops-intellipaat/merge-conflict',
 'rmtheis/tess-two',
 'pwn20wndstuff/Undecimus',
 'xianyi/OpenBLAS',
 'skywind3000/kcp',
 'kbengine/kbengine',
 'libgit2/libgit2',
 'nonstriater/Learn-Algorithms',
 'Mbed-TLS/mbedtls',
 'pbatard/rufus',
 'phpredis/phpredis',
 'nmap/nmap',
 'fw876/helloworld',
 'twitter/twemproxy']

headers = {"Authorization": f"token {token}", "User-Agent": username}


def github_api_request(url: str) -> Union[List, Dict]:
    response = requests.get(url, headers=headers)
    response_data = response.json()
    if response.status_code != 200:
        raise Exception(
            f"Error response from github api! status code: {response.status_code}, "
            f"response: {json.dumps(response_data)}"
        )
    return response_data


def get_repo_language(repo: str) -> str:
    url = f"https://api.github.com/repos/{repo}"
    repo_info = github_api_request(url)
    if type(repo_info) is dict:
        repo_info = cast(Dict, repo_info)
        return repo_info.get("language", None)
    raise Exception(
        f"Expecting a dictionary response from {url}, instead got {json.dumps(repo_info)}"
    )


def get_repo_contents(repo: str) -> List[Dict[str, str]]:
    url = f"https://api.github.com/repos/{repo}/contents/"
    contents = github_api_request(url)
    if type(contents) is list:
        contents = cast(List, contents)
        return contents
    raise Exception(
        f"Expecting a list response from {url}, instead got {json.dumps(contents)}"
    )


def get_readme_download_url(files: List[Dict[str, str]]) -> str:
    """
    Takes in a response from the github api that lists the files in a repo and
    returns the url that can be used to download the repo's README file.
    """
    for file in files:
        if file["name"].lower().startswith("readme"):
            return file["download_url"]
    return ""


def process_repo(repo: str) -> Dict[str, str]:
    """
    Takes a repo name like "gocodeup/codeup-setup-script" and returns a
    dictionary with the language of the repo and the readme contents.
    """
    contents = get_repo_contents(repo)
    readme_contents = requests.get(get_readme_download_url(contents)).text
    return {
        "repo": repo,
        "language": get_repo_language(repo),
        "readme_contents": readme_contents,
    }


def scrape_github_data() -> List[Dict[str, str]]:
    """
    Loop through all of the repos and process them. Returns the processed data.
    """
    return [process_repo(repo) for repo in repos]


if __name__ == "__main__":
    data = scrape_github_data()
    json.dump(data, open("data2.json", "w"), indent=1)
    
# get data frame
def get_data():
    ''' Retrieves dataframe with repo name, repo language, and the readme contents'''

    return pd.read_json("data2.json")

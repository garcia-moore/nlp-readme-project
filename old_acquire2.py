import os
 import pandas as pd
 import json
 from typing import Dict, List, Optional, Union, cast
 import requests
 from env import token, username

 url = "https://api.github.com/search/repositories"

 repos = ['BeatSwitch/lock',
  'Boostport/kubernetes-vault',
  'Hitomis/SpinMenu',
  'IBDecodable/IBLinter',
  'KieranLafferty/KLNoteViewController',
  'KittenYang/KYCuteView',
  'LinkedInAttic/camus',
  'ModusCreateOrg/budgeting',
  'NewAmsterdamLabs/ZOZolaZoomTransition',
  'OverZealous/run-sequence',
  'RisingStack/node-style-guide',
  'StevenSLXie/Tutorials-for-Web-Developers',
  'Sutto/rocket_pants',
  'SwiftGGTeam/Developing-iOS-9-Apps-with-Swift',
  'Tangdixi/DCPathButton',
  'TeehanLax/Upcoming',
  'Urigo/merge-graphql-schemas',
  'aaditmshah/augment',
  'akkyie/AKPickerView',
  'amplab/shark',
  'android-cn/android-open-project-demo',
  'angular-google-chart/angular-google-chart',
  'at-import/toolkit',
  'atljeremy/JFMinimalNotifications',
  'autresphere/ASMediaFocusManager',
  'benhowdle89/svgeezy',
  'binaryfork/Spanny',
  'binoculars/aws-lambda-ffmpeg',
  'boztalay/BOZPongRefreshControl',
  'btford/ngmin',
  'burgessjp/ThemeSkinning',
  'cbrauckmuller/helium',
  'cds-snc/covid-alert-app',
  'celluloid/celluloid-io',
  'chrisbanes/photup',
  'christianroman/CRGradientNavigationBar',
  'cundong/ZhihuPaper',
  'danthorpe/Money',
  'diracdeltas/sniffly',
  'dodola/WeexOne',
  'dtorres/OLImageView',
  'dylang/grunt-notify',
  'ehazlett/interlock',
  'elevation/event_calendar',
  'estelle/clowncar',
  'fastlane-old/frameit',
  'filamentgroup/loadJS',
  'gdotdesign/elm-ui',
  'go-xorm/xorm',
  'googlearchive/ChromeWebLab',
  'harrystech/prelaunchr',
  'heroku/logplex',
  'hxgf/smoke.js',
  'iconic/SVGInjector',
  'ipython-books/cookbook-code',
  'jakerella/jquery-mockjax',
  'jboesch/Gritter',
  'jeromegn/DocumentUp',
  'jirsbek/SSH-keys-in-macOS-Sierra-keychain',
  'johnno1962/Refactorator',
  'jsmreese/moment-duration-format',
  'kahopoon/Pokemon-Go-Controller',
  'kenkeiter/skeuocard',
  'krzysztofzablocki/Traits',
  'kzk/unicorn-worker-killer',
  'l20n/l20n.js',
  'laserlemon/vestal_versions',
  'leonidas/transparency',
  'less/less.ruby',
  'lgtmco/lgtm',
  'ltebean/LTInfiniteScrollView',
  'luojilab/radon-ui',
  'ly4k/CurveBall',
  'mailman/mailman',
  'markgoodyear/headhesive.js',
  'maxzhang/maxzhang.github.com',
  'mikemintz/react-rethinkdb',
  'mjibson/goread',
  'mjsarfatti/nestedSortable',
  'mmangino/facebooker',
  'nicklockwood/AsyncImageView',
  'ninjinkun/NJKScrollFullScreen',
  'noahlevenson/stealing-ur-feelings',
  'oikomi/FishChatServer',
  'olahol/reactpack',
  'ole/OBShapedButton',
  'ole/whats-new-in-swift-4-2',
  'pavelk2/social-feed',
  'pguso/js-plugin-circliful',
  'playgameservices/android-basic-samples',
  'rcrowley/go-tigertonic',
  'schani/clojurec',
  'smalldots/smalldots',
  'stefanjauker/BadgeView',
  'stolksdorf/Parallaxjs',
  'svrcekmichal/redux-axios-middleware',
  'technomancy/emacs-starter-kit',
  'typelevel/simulacrum',
  'vfaronov/httpolice',
  'ycd/dstp']

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

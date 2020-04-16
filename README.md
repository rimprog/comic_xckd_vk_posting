# Comics publisher

This script download random xckd comic page from [xkcd.com](https://xkcd.com/) and post it on vk group wall.
All data fetches from [xkcd API](https://xkcd.com/json.html) and posting with [VK API](https://vk.com/dev). Just use console command `python3 main.py`.

### How to install

You need get VK access_token. To do this, follow these steps:
1. [Create](https://vk.com/groups?tab=admin) your VK Group
2. [Register](https://vk.com/editapp?act=create) your standalone-application and link your created early vk group
3. Go through the [Implicit Flow procedure](https://vk.com/dev/implicit_flow_user) and get access_token with photos, groups, wall and offline permissions (scope parameter in VK API)
If you are unable to do this, read the additional information in the [VK API Manuals](https://vk.com/dev/manuals).

After get access_token, create .env file in root project folder and place access_token in VK_ACCESS_TOKEN variable. 
Also add your vk group id in VK_GROUP_ID variable. Your vk group id you can look [here](https://regvk.com/id/)

Example .env:
```
VK_GROUP_ID=YOUR_VK_GROUP_ID
VK_ACCESS_TOKEN=YOUR_VK_ACCESS_TOKEN
```

Python3 should be already installed. 
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).

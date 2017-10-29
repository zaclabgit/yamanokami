from slackbot.bot import listen_to 

@listen_to(r'だめ|ダメ|あかん|つらい|しんどい|きつい')
def support_by_syuzo(message):
    post = {
            "title" : "",
            "color": "#FF0000",
            "image_url": "http://livedoor.4.blogimg.jp/jin115/imgs/e/1/e15ed397.jpg"
    }
    ret = message._client.webapi.chat.post_message(
        message._body['channel'],
        '',
        username=message._client.login_data['self']['name'],
        as_user=True,
        attachments=[post]
    )
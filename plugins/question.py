# -*- coding: utf-8 -*-
from slackbot.bot import respond_to
import csv

EMOJIS = (
    'one',
    'two',
    'three',
    'four',
    'five',
)

@respond_to('質問/(.*)')
def poll(message, params):
    args = [row for row in csv.reader([params], delimiter='/')][0]
    if len(args) < 3:
        message.reply('使用方法: 質問/タイトル/質問内容/[項目（5つまで）/ ...]')
        return

    # print(args)
    title = args.pop(0)
    naiyou = args.pop(0)
    options = []
    for i, o in enumerate(args):
        options.append('* :{}: {}'.format(EMOJIS[i], o))

    # ref https://github.com/lins05/slackbot/issues/43
    send_user = message.channel._client.users[message.body['user']][u'name']
    post = {
        'pretext': '{}からの質問'.format(send_user),
        'title': title,
        'author_name': send_user,
        'text': naiyou + '\n' + '\n'.join(options),
        'color': 'good'
    }

    ret = message._client.webapi.chat.post_message(
        message._body['channel'],
        '',
        username=message._client.login_data['self']['name'],
        as_user=True,
        attachments=[post]
    )
    ts = ret.body['ts']

    for i, _ in enumerate(options):
        message._client.webapi.reactions.add(
            name=EMOJIS[i],
            channel=message._body['channel'],
            timestamp=ts
        )


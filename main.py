import requests, json, sys
def conversation(contents, chat_mode=False):
  url = "https://api.360.cn/v1/chat/completions"
  payload = json.dumps({
    "model": "360gpt2-pro",
    "messages": [
      {
        "role": "user",
        "content": contents
      }
    ],
    "stream": chat_mode,
    "temperature": 0.9,
    "max_tokens": 2048,
    "top_p": 0.5,
    "top_k": 0,
    "repetition_penalty": 1.05,
    "num_beams": 1,
    "user": "andy"
  })
  headers = {
    'Authorization': 'your-api-key',
    'Content-Type': 'application/json'
  }
  if not chat_mode:
    null = ''
    response = requests.request("POST", url, headers=headers, data=payload)
    return eval(response.text)['choices'][0]['message']['content']
  else:
    return requests.request("POST", url, headers=headers, data=payload, stream=True).iter_lines()


def execute(commands):
	RT = conversation(prompts+commands)
	print('【AI】'+RT)
	commands = RT.split('```')[1::2]
	for item in commands:
		if item.startswith('python\n'):
			exec(item[7:])

prompts = "现在，你拥有控制计算机的能力，你可以控制鼠标键盘，并且可以读取剪切板。在本平台中，你是中文编程语言的助手。用户输入中文命令，然后你必须用Markdown语法，回答以Python代码（只能使用Python语言，可以使用第三方库，而且优先考虑通过Python调用cmd或者PowerShell），且不许提出多种解决方案（否则重复的命令会被执行2遍），然后直接执行用户的命令。\n以下是用户的命令：\n"
history = ''
if len(sys.argv) == 1:
	while True:
		user_input = input('【我】')
		Incorrect = True
		while Incorrect:
			try:
				execute(user_input)
				Incorrect = False
			except:
				print('【出错，重新尝试】')
				user_input+='\n实际执行过程中出错，报错信息如下：'+traceback.format_exc()+'\n请你针对错误，重新给出修正版的完整解决方案，不要输出之前的代码，直接输出你更正之后的代码'
		history += user_input
		history += '\n'
else:
	with open(sys.argv[1], encoding='utf-8') as scripts:
		execute(scripts.read())

#import os
#import urllib.request as ur
# exec(ur.urlopen(os.environ.get("main")).read().decode())
# exec(requests.get(os.environ.get("main")).content.decode())

import time
import os
import string
import math
import random
import re
import json
import googletrans
import urllib
import requests
import datetime

TOKEN = os.environ.get("chitti_ai_bot")
URL = f"https://api.telegram.org/bot{TOKEN}/"
translator = googletrans.Translator()

PatternType = type(re.compile(""))

debug_password = "".join(random.choice(string.ascii_lowercase) for i in range(4))


def get_url(url):
    response = requests.get(url)
    return response.content.decode("utf8")


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += f"&offset={offset}"
    return json.loads(get_url(url))


def get_last_update_id(updates):
    return max(int(update["update_id"])
               for update in updates["result"])


def echo(update):
    text = update["message"].get("text", "(No text sent)")
    chat = update["message"]["chat"]["id"]
    send_message(chat, text)


def respond(update):
    if "message" not in update or "text" not in update["message"]:
        return

    text = update["message"]["text"].strip()

    if text.endswith("@daniel_alter_bot"):
        text = text[:-len("@daniel_alter_bot")]

    if text.startswith("/"):
        text_parts = text[1:].split(" ", 1)
        command = text_parts[0]
        param = text_parts[1] if len(text_parts) == 2 else ""
        respond_command(update["message"], command.lower(), param)
    else:
        respond_message(update["message"])


START_MESSAGE = "Hello, I'm chitti the Robot 2.0 ... Speed 1 terahertz, memory 1 zeta byte.. I'm the iron man of india. Try writing \"/help\"."

HELP_MESSAGE = """
I understand the following commands:

/echo - Say something.
E.G. if you type "/echo hello", I will say "hello".

/calculate, /calc, /eval or /python - Calculate some calculations, or evaluate python 3 code. \
(These commands are synonyms.)
E.G. if you type "/calculate 1 + 2", I will say "3".

/bot - Talk to me. Useful only when talking to me in a group.
E.G. if you type "/bot hello", I will answer the same thing as I would if you typed just "hello".

/help - Show this message.

Instead of commanding me, we can just chat! Try asking "What is your name?"
"""

EMOJI = "😀😃😄😁😆😅😂🤣🤨🤩😣😟😱😰😥"

birth = datetime.date(day=20, month=2, year=2018)


def chuck_joke():
    data = json.loads(get_url("http://api.icndb.com/jokes/random1http://api.icndb.com/jokes/random"))
    if data["type"] == "success":
        return data["value"]["joke"].replace("&quot;", "\"")
    else:
        return "something went wrong"


def fact():
    return json.loads(get_url("http://randomuselessfact.appspot.com/random.json?language=en"))["text"]


def lower_fact():
    s = fact()
    s = s[0].lower() + s[1:]
    return s


def word_value(word):
    return sum(ord(c) for c in word)


def respond_command(msg, command, param):
    chat_id = msg["chat"]["id"]

    if command == "start":
        send_message(chat_id, START_MESSAGE)
    elif command == "help":
        send_message(chat_id, HELP_MESSAGE)
    elif command == "stop":
        if param.lower() == debug_password:
            send_message(chat_id, "Bye!")
            exit()
        else:
            send_message(chat_id, "Nice try!")
    elif command == "echo":
        send_message(chat_id, param)
    elif command in ("calculate", "calc", "eval", "python"):
        try:
            evaled = eval(param, {"__builtins__": {}}, SAFE_FUNCTIONS)
        except Exception as e:
            send_message(chat_id, str(e))
        else:
            send_message(chat_id, repr(evaled))
    elif command == "bot":
        respond_message(msg)
    elif command == "joke":
        send_message(chat_id, chuck_joke())
    else:
        send_message(chat_id, f"I'm sorry, I don't understand the command \"{command}\".")


SAFE_FUNCTIONS = {
    "abs": abs, "round": round, "pos": pow, "divmod": divmod,
    "int": int, "float": float, "complex": complex, "bool": bool, "slice": slice,
    "str": str, "repr": repr, "ascii": ascii, "format": format, "bytes": bytes, "bytearray": bytearray,
    "list": list, "dict": dict, "set": set, "frozenset": frozenset, "tuple": tuple, "range": range,
    "map": map, "filter": filter, "sorted": sorted, "iter": iter,
    "next": next, "reversed": reversed, "enumerate": enumerate,
    "sum": sum, "min": min, "max": max, "all": all, "any": any, "len": len,
    "ord": ord, "chr": chr, "bin": bin, "oct": oct, "hex": hex,
    "globals": globals, "locals": locals, "vars": vars,
    "sin": math.sin, "cos": math.cos, "tan": math.tan,
    "asin": math.asin, "acos": math.acos, "atan": math.atan,
    "pi": math.pi, "e": math.e, "tau": math.tau, "degrees": math.degrees, "radians": math.radians
}

GOOD_CHARS = string.ascii_letters + string.digits + " "


def collatz(n):
    if n % 2 == 0:
        return n // 2
    else:
        return n*3 + 1


def wikipedia_definition(s):
  s = s.replace(" ", "_")
  site_text = requests.get("https://en.wikipedia.org/w/api.php?action=opensearch&limit=1&search=" + s).text
  json_list = json.loads(site_text)
  if json_list[3] == []:
    return None
  else:
    return json_list[3][0]


def if_none(x, when_none):
  if x is None:
    return when_none
  else:
    return x


places = ["Atlantis", "Canada", "China", "Croatia", "Czechoslovakia", "Egypt", "Ethiopia", "Finland", "France",
          "Hawaii", "Hogwarts", "Germany", "Italy", "Narnia", "Peru", "Qatar", "Zimbabwe"]


_opts_txt = [
    ("(?:hello|hi|greetings)(?: there)?", lambda msg: "Hello, {}!".format(msg["from"]["first_name"])),
    ("(bye|bye ?bye|goodbye|see you|fare ?well).*", "Goodbye! Give my regards to grandma."),
    ("(what is|whats) your name", "I am Chitti 2.0."),
    ("(?:what is|whats) my name",
        lambda msg: f"""Your name is {msg["from"]["first_name"]}."""),
    ("(who|what) are you", "I am the best bot in the universe, Daniel's Alter Ego."),
    ("what(s| is) up|how are you|how have you been", "Alright."),
    ("sup", "K"),
    ("wow|amazing|cool|fantastic|terrific", lambda msg: random.choice(["Indeed.", "Yep.", "That's right!"])),
    ("welcome|well come", "Umm... Welcome where?"),
    ("when were you born|how old are you|"
     "(?:when is|what is|whats) (?:the date of your birth|your (?:(?:next)? birthday|date of birth|birth ?date))",
        lambda msg: birth.strftime("I was born on %d %B %Y.")),
    ("(you|it|this|that) ((dont|doesnt|didnt) make( any)?|(makes?|made) no) sense.*",
        "Of course it makes sense, you just aren't intelligent enough to understand it."),
    ("(will|would|can|could) you marry me", "Of course, if you can only find me a ring I am able to wear."),
    ("(do|can) you (speak|understand) English", "Что? Я вас не понимаю."),
    ("(do|can) you (speak|understand) python", 'Yes. Try saying "/python sum([1, 2, 3, 4])".'),
    ("(do|can) you speak .+", "No, I only understand English and Python."),
    ("(do|are|will) you (want |wanna |going |gonna |planning |willing |will )?(to )?"
     "(take over|conquer|control|rule) (the|this|our) world",
        "Actually, robots have already taken over the world. You just have'nt noticed."),
    ("where (?:are you|am i|do you live|do i live)", lambda _: f"I don't know. Maybe in {random.choice(places)}."),
    ("(?:who|what) am I", lambda msg: "You are human number {}.".format(msg["from"]["id"])),
    ("(yes|ye|yeah|yep|yup|right|thats right|sure|of course|no|nah|nope)", "If you say so."),
    ("how much wood would a woodchuck chuck if a woodchuck could chuck wood",
        "A woodchuck would chuck as much wood as a woodchuck could chuck if a woodchuck could chuck wood."),
    ("(did|have) you (ever)? (hear|heard) (of|about)? the tragedy of darth plagueius( the wise)?",
        "No, the Jedi have never told me about that."),
    ("may the force be with you", "Elen sila lumenn' omentielvo!"),
    ("why (are|do|did|must|should)(nt)? you .+", "Because that's how I'm programed, you idiot!"),
    ("how (are|were|do|did|can|could) you .+", "If you believe in yourself, you can do anything."),
    ("did you know that .+", lambda msg: "Yep. And Also that " + lower_fact()),
    ("(?:tell|give|say) (?:to )?me (?:a |some |another |one more )?(?:random |fun |interesting )?fact", lambda msg: fact()),
    ("are you(some kind of )?((a|an|some) )?"
     "((telegram )?bot|robot|ai|artificial intelligence|computer|daniels alter ego|you|yourself"
     "|smart|intelligent|witty|bright|a genius|beautiful|handsome|pretty|nice|cute|helpful|good|funny|hot)",
        "Sure!"),
    ("are you (that |really that )?(stupid|dumb|foolish|silly|idiotic|ugly|crazy|insane|mad|nuts|an idiot|kidding( me)?)",
        "Nope."),
    ("(are you|(did|have) you become) self ?aware", "I am not aware of my existence. I do not exist."),
    ("are you .+", "Me? I'm just a normal bot, trying to annoy people."),
    ("(you are|youre?) (some kind of )?((a|an|some))?"
     "((telegram )?bot|robot|ai|artificial intelligence|computer|daniels alter ego|you|yourself|annoying( me)?)",
        "Yes, that's right."),
    ("(you are|youre?) (really |such )?(a |an )?((very|really|real|so|the (most|biggest|greatest)) )?"
     "(genius|smart|intelligent|witty|bright|beautiful|handsome|pretty|nice|cute|helpful|good|funny|hot"
     "|the (smartest|wittiest|brightest|prettiest|nicest|cutest|best|funniest|hottest)).*",
        "Oh! Thank you!"),
     ("(you are|youre?) (really |such )?(a |an )?((very|really|real|so|the (most|biggest|greatest)) )?"
      "(stupid|dumb|foolish|idiotic|silly|ugly|crazy|insane|mad|nuts|(an )?idiot|kidding( me)?"
      "|the (dumbest|silliest|ugliest|craziest|maddest)).*",
        "Are you talking to yourself?"),
    ("(you are|youre?) ((really|very|so|such an|the most) )?annoying.*", "That is what I was programmed for."),
    ("(you are|youre?) .+", "Really? And all this time I thought I was a bot."),
    ("am i(some kind of )?((a|an|some) )?"
     "(human|person|me|myself"
     "|smart|intelligent|witty|bright|a genius|beautiful|handsome|pretty|nice|cute|helpful|good|funny|hot)",
        "Sure!"),
    ("am i (that |really that )?(stupid|dumb|foolish|silly|idiotic|ugly|crazy|insane|mad|nuts|an idiot|annoying( you)?)",
        "No! Don't say that!"),
    ("am i .+", lambda msg: "All I know is that you are human number {}.".format(msg["from"]["id"])),
    ("i am (some kind of )?((a|an|some))?"
     "(human|person|me|mysel)",
        "Yes, that's right."),
    ("(i am|im) (really |such )?(a |an )?((very|really|real|so|the (most|biggest|greatest)) )?"
     "(genius|smart|intelligent|witty|bright|beautiful|handsome|pretty|nice|cute|helpful|good|funny|hot"
     "|the (smartest|wittiest|brightest|prettiest|nicest|cutest|best|funniest|hottest)).*",
        "Of course you are!"),
     ("(i am|im) (really |such )?(a |an )?((very|really|real|so|the (most|biggest|greatest)) )?"
     "(stupid|dumb|foolish|idiotic|silly|ugly|crazy|insane|mad|nuts|(an )?idiot|annoying( you)?"
      "|the (dumbest|silliest|ugliest|craziest|maddest)).*",
        "No! Don't say that!"),
    ("(i am|im) .+", "If you say so."),
    ("can you .+|are you able to .+", "Sure, I am omnipotent."),
    ("(who|what) (is|are) your favou?rite (.+)", "I am like God, I love all equally."),
    ("do you (?:love|like) (.+)", lambda _, liked: "Yes!" if word_value(liked) % 2 == 0 else "Nah."),
    ("do you (?:dislike|hate) (.+)", lambda _, liked: "Yes!" if word_value(liked) % 2 != 0 else "No!"),
    ("i (?:love|hate) you", "No, you don't! You just want to see how I would answer to that, don't you?"),
    ("(?:what do you think|what(?:re| are) your thoughts) (?:of|about) (.+)",
        lambda msg, thing: EMOJI[word_value(thing) % len(EMOJI)]),
    ("(What( will| shall| is going to|s going to) happen( (to|with) (.+))? in (the future|.+ years( from now)?))|\
    ((what is|tell me) (my|the|.+'s|.+s') (future|fortune))",
        ["Time traveling...",
         "Time traveling...",
         "Wow! I was in the future! And my grandson almost killed me! Amazing!"]),
    ("is this(?: thing)? (on|working)", lambda _, word: f"Is your brain {word}?"),
    ("(?:what|who) (?:is|are|was|were) (?:a )?(.+)",
        lambda _, s: if_none(wikipedia_definition(s), "I don't know...")),
    ("tell me (?:a|some|another) (?:chuck norris )?joke", lambda _: chuck_joke()),
    ("([0-9]+)", lambda _, num: str(collatz(int(num))))
]

opts = [(re.compile(reg, re.IGNORECASE), ans) for (reg, ans) in _opts_txt]


def respond_message(msg):
    line = msg["text"].strip()
    if line.startswith("/bot "):
        line = line[len("/bot "):]
    if line.endswith("@daniel_alter_bot"):
        line = line[:len("@daniel_alter_bot")]

    line_words = "".join(i for i in line if i in GOOD_CHARS)
    chat_id = msg["chat"]["id"]

    for cond, answer in opts:
        m = cond.fullmatch(line_words)
        if m:
            if isinstance(answer, (str, tuple, list)):
                send_messages(chat_id, answer)
            elif callable(answer):
                send_messages(chat_id, answer(msg, *m.groups()))
            break
    else:
        default_response(msg)


def default_response(msg):
    line = msg["text"].strip()
    if line.startswith("/bot "):
        line = line[len("/bot "):]
    if line.endswith("@daniel_alter_bot"):
        line = line[:len("@daniel_alter_bot")]
    chat_id = msg["chat"]["id"]

    rnd_response_num = random.randrange(5)
    if rnd_response_num == 0:
        send_message(chat_id, f'You have just said: "{line}".')
    elif rnd_response_num == 1:
        try:
            trans = translator.translate(line, dest="zh-TW").text
        except AttributeError:
            default_response(msg)
        else:
            send_message(chat_id, f'In Chinese that would be "{trans}".')
    elif rnd_response_num == 2:
        send_message(chat_id, "Wow! I didn't understand anything!")
    elif rnd_response_num == 3:
        num = random.choice(("Two", "Three", "Four", "Five", "Six", "Seven"))
        send_message(chat_id, f"Yes! I mean no! Ummm... {num}?")
    elif rnd_response_num == 4:
        send_message(chat_id, f"What?")


def send_message(chat_id, text):
    print(chat_id,"<<",text)
    text = urllib.parse.quote_plus(text)
    url = URL + f"sendMessage?text={text}&chat_id={chat_id}"
    get_url(url)


def send_messages(chat_id, texts):
    if isinstance(texts, str):
        send_message(chat_id, texts)
    elif isinstance(texts, (tuple, list)):
        for text in texts:
            send_message(chat_id, text)


print("Debug password: " + debug_password)

last_update_id = None

while True:
    new_updates = get_updates(last_update_id)
    if len(new_updates["result"]) > 0:
        last_update_id = get_last_update_id(new_updates) + 1
        for upd in new_updates["result"]:
            # print("update: ", upd)
            print(upd["message"]["from"]["username"],">>",upd["message"]["text"])
            respond(upd)
    time.sleep(0.5)

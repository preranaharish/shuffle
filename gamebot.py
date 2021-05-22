import os
import random
import discord
import configly
from configly import errors
# from dotenv import load_dotenv
from urllib.request import urlopen

easy = open("easy.txt")
words = easy.read().splitlines()
# load_dotenv()
# TOKEN = os.getenv('GAMEBOT_TOKEN')
client = discord.Client()
TOKEN = os.environ.get('GAMEBOT_TOKEN')

global total_points,n
total_points = 0
n = 0
def change_words():
    global words
    word_url = "https://www.mit.edu/~ecprice/wordlist.10000"
    response = urlopen(word_url)
    long_txt = response.read().decode()
    words = long_txt.splitlines()

def shuffle_word(word):
    jumble = ""
    while word:
        position = random.randrange(len(word))
        jumble += word[position]
        word = word[:position] + word[(position + 1):]
    if word == jumble:
        shuffle_word(word) 
    return jumble

def generate_word():
    if total_points == 100 or total_points == 105:
        change_words()
    status = True
    while status:
        word = random.choice(words)
        if len(word)>=4:
            shuffled_word = shuffle_word(word)
            status = False
            corr_word = word
            shuffled = shuffle_word
    return word,shuffled_word
    
def evaluate(correct,received):
    global total_points
    if correct.lower()==received.lower():
        cor_incor = True
        total_points +=10
    else:
        cor_incor = False
        total_points -=5
    return total_points,cor_incor


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    appreciation_words = ["Keep working on it. You're good.",
                        "Aren't you proud of yourself?",
                        "Wow!","Nothing can stop you now.",
                        "I knew you could do it.",
                        "Great!"]

    encouraging_words = ["Don't give up.",
                        "Never give up.",
                        "Come on! You can do it!.",
                        "Believe in yourself."]
    start_words = ['hi','hello']
    received_text = str(message.content).lower()
    global corr_word
    global shuffled
    global n
    global total_points

    try:
        if received_text in start_words:
            welcome_msg = "Hello!,Welcome to Shuffle"
            help_text = "Type help if you are struck!!"
            msg = "Enter '?play' to start playing"
            embedVar = discord.Embed(title="SHUFFLE", description=welcome_msg, color=0x00ff00)
            embedVar.add_field(name="How to Play?",value=msg, inline=False)
            await message.channel.send(embed=embedVar)
            embedhelp = discord.Embed(title="HELP!!!!!!!!!!!", description=help_text, color=0xf50511)
            await message.channel.send(embed=embedhelp)

        if received_text.startswith('?play'):
            instructions="Enter your answer preceeded with ?ans followed by a space\n" + \
            "Example:?ans shuffle\n For every right answer you get 10 points\n" + \
            "For every wrong answer you lose 5 points\n" + \
            "Type in ?quit to stop the game\n\n Good Luck!!!!!!!\nPut your Thinking Caps On " + str("🤓")
            embedInst = discord.Embed(title="Instructions", description=instructions, color=0x00ff00)
            await message.channel.send(embed=embedInst)

            corr_word,shuffled = generate_word()
            n = 1
            title_text = "SHUFFLE "+"#"+str(1)
            embedword = discord.Embed(title=title_text, description=shuffled, color=0xfc0373)
            await message.channel.send(embed=embedword)


        if received_text.startswith('?ans'):
            rec_word = received_text.split(" ")[1]
            points_obt,cor_stat = evaluate(corr_word,rec_word)
            if cor_stat:
                corr_text = "Points="+str(points_obt)
                emoji = "✅"
                title_ = "You are Right!!  "+ str(emoji)
                embedword = discord.Embed(title=title_, description=corr_text, color=0x077501)
                embedword.add_field(name=random.choice(appreciation_words), value="\u200b",inline=False)
                await message.channel.send(embed=embedword)
                corr_word,shuffled = generate_word()
                n += 1
                title_text = "SHUFFLE "+"#"+str(n)
                embed_new_word=discord.Embed(title=title_text, description=shuffled, color=0x017571)
                await message.channel.send(embed=embed_new_word)

            else:
                in_corr_text = "Points="+str(points_obt)
                emoji = "❌"
                title_ = "You are Wrong!!  "+ str(emoji)
                embedword = discord.Embed(title=title_, description=in_corr_text, color=0xf50511)
                embedword.add_field(name=random.choice(encouraging_words), value="\u200b",inline=False)
                embedword.add_field(name="Correct Answer is:", value=corr_word)
                await message.channel.send(embed=embedword)
                corr_word,shuffled = generate_word()
                n += 1
                title_text = "SHUFFLE "+"#"+str(n)
                embed_new_word=discord.Embed(title=title_text, description=shuffled, color=0x017571)
                await message.channel.send(embed=embed_new_word)


        if received_text == '?quit':
            embedquit = discord.Embed(title="Bye!!!!", description="Hope you enjoyed Playing SHUFFLE\nHave a great day", color=0xf50511)
            await message.channel.send(embed=embedquit)

        if received_text == 'help':
            embedVar = discord.Embed(title="I'm here to Help you", description="Type Hi or Hello to know about Shuffle", color=0x00ff00)
            await message.channel.send(embed=embedVar)

        elif len(received_text)>=1 and received_text not in['hi','hello','?quit','help','?play'] and received_text.split()[0] != '?ans':
            help_text = "Type help if you are struck!!"
            msg = "Enter '?play' to start playing\nEnter your answer preceeded with ?ans followed by a space\n" + \
            "Example:?ans shuffle"
            embedVar = discord.Embed(title="Oops!!!", description="Something went wong\nLet's Try Again\n"+ help_text, color=0x00ff00)
            embedVar.add_field(name="How to Play?",value=msg, inline=False)
            await message.channel.send(embed=embedVar)
        
        else:
            pass

    except:
        embedVar = discord.Embed(title="Something went wrong", description="Type Hi or Hello to know about Shuffle", color=0x00ff00)
        await message.channel.send(embed=embedVar)



client.run(TOKEN)

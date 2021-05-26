import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
from urllib.request import urlopen
from discord.ext.commands.errors import MissingRequiredArgument

# to deploy on server uncomment the below lines
# import configly
# TOKEN = os.environ.get('GAMEBOT_TOKEN')

#create a .(dot)env file and store your bot token as GAMEBOT_TOKEN
load_dotenv()
TOKEN = os.getenv('GAMEBOT_TOKEN')


#creating a client object
client = commands.Bot(command_prefix="?")
total_points = 0
n = 0
gameOver = True
player = ""
corr_word = ""
shuffled = ""
word_url = "https://www.mit.edu/~ecprice/wordlist.10000"
response = urlopen(word_url)
long_txt = response.read().decode()
words = long_txt.splitlines()


def shuffle_word(word):
    """Function to shuffle the letter of the randomly generated word,even after shuffling,if the same word is generated,
    the function is called again recursively """
    jumble = ""
    while word:
        position = random.randrange(len(word))
        jumble += word[position]
        word = word[:position] + word[(position + 1):]
    if word == jumble:
        shuffle_word(word) 
    return jumble

def generate_word():
    """Function to generate a word randomly"""
    status = True
    while status:
        word = random.choice(words)
        if len(word)>=4:
            shuffled_word = shuffle_word(word)
            status = False
            if shuffle_word==word:
                status = True
    return word,shuffled_word
    
def evaluate(correct,received,play):
    """To check if the answer is right"""
    global total_points
    if play == player:
        if correct.lower()==received.lower():
            cor_incor = True
            total_points +=10
        else:
            cor_incor = False
            total_points -=5
        return total_points,cor_incor



@client.command()
async def shuffle(message,p1: discord.Member):
    try:

        global gameOver
        global player
        global n
        global corr_word
        global shuffled
        global total_points


        if message.author == client.user:
            return
        elif gameOver:
            total_points = 0
            gameOver = False
            player = p1

            await message.send("Starting a game with "+str(message.author))
            welcome_msg = "Hello!,Welcome to Shuffle\nSHUFFLE is a simple word puzzle where you find the correct word from a scrambled set of letters. You need to use all the given letters."
            help_text = "Type help if you are struck!!"
            embedVar = discord.Embed(title="SHUFFLE", description=welcome_msg, color=0x00ff00)
            embedVar.add_field(name="HELP!!!!!!!!!!!",value=help_text, inline=False)
            await message.send(embed=embedVar)

            instructions="* Enter your answer preceeded with ?ans followed by a space\n\n" + \
                "* On seeing a jumbled word,All you have to do is to unjumble it to frame a correct word\n\n"+ \
                "* Once you find the correct word,Type in your answer as per the instructions\n\n"+ \
                "Example:fsuehlf\n\nOn re-jumbling,it gives'shuffle'\n\n" + \
                "You should type\n?ans shuffle\n\n* If you don't know the answer type ?ans idk\n\n* For every right answer you get 10 points\n\n" + \
                "* For every wrong answer you lose 5 points\n\n" + \
                "* Type in ?quit to stop the game\n\n Good Luck!!!!!!!\nPut your Thinking Caps On " + str("🤓")
            embedInst = discord.Embed(title="Instructions", description=instructions, color=0x00ff00)
            await message.send(embed=embedInst)

            corr_word,shuffled = generate_word()
            rec_stat = False
            n = 1
            title_text = "SHUFFLE "+"#"+str(1)
            embedword = discord.Embed(title=title_text, description=shuffled, color=0xfc0373)
            await message.send(embed=embedword)

        else:
            await message.send("A game is already in progress! Finish it before starting a new one.")
    except MissingRequiredArgument:
        await message.send("One player is required type  ?shuffle @<your account>")
    except:
        await message.send("Something went wrong! Try Again")




@client.command()
async def ans(message,answer):
    global corr_word
    global n
    global gameOver

    appreciation_words = ["Keep working on it. You're good.",
                        "Aren't you proud of yourself?",
                        "Wow!","Nothing can stop you now.",
                        "I knew you could do it.",
                        "Great!"]

    encouraging_words = ["Don't give up.",
                        "Never give up.",
                        "Come on! You can do it!.",
                        "Believe in yourself."]

    if not(gameOver):
        if message.author==player:
            points_obt,cor_stat = evaluate(corr_word,answer,player)
            if cor_stat:
                corr_text = "Points="+str(points_obt)
                emoji = "✅"
                title_ = "You are Right!!  "+ str(emoji)
                embedword = discord.Embed(title=title_, description=corr_text, color=0x077501)
                embedword.add_field(name=random.choice(appreciation_words), value="\u200b",inline=False)
                await message.send(embed=embedword)

                if n<10:
                    corr_word,shuffled = generate_word()
                    n += 1
                    title_text = "SHUFFLE "+"#"+str(n)
                    embed_new_word=discord.Embed(title=title_text, description=shuffled, color=0x017571)
                    await message.send(embed=embed_new_word)
                else:
                    await message.send("You have already answered 10 puzzles\nHope you enjoyed playing Shuffle\nCall me again to continue playing")   
            #if the user gives an incorrect answer
            else:
                in_corr_text = "Points="+str(points_obt)
                emoji = "❌"
                title_ = "You are Wrong!!  "+ str(emoji)
                embedword = discord.Embed(title=title_, description=in_corr_text, color=0xf50511)
                embedword.add_field(name=random.choice(encouraging_words), value="\u200b",inline=False)
                embedword.add_field(name="Correct Answer is:", value=corr_word)
                await message.send(embed=embedword)
                if n<10:
                    corr_word,shuffled = generate_word()
                    n += 1
                    title_text = "SHUFFLE "+"#"+str(n)
                    embed_new_word=discord.Embed(title=title_text, description=shuffled, color=0x017571)
                    await message.send(embed=embed_new_word)
                    
                else:
                    gameOver = True
                    await message.send("You have already answered 10 puzzles\nHope you enjoyed playing Shuffle\nCall me again to continue playing")

    else:
        await message.send("Please start a new game using the ?shuffle @<your account> command.")

@client.command()
async def quit(message):
    global gameOver
    gameOver = True
    await message.send("Thank you for playing.")


client.run(TOKEN)

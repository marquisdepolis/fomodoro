# fomo doro
The best way to keep yourself on task with the help of LLMs
![Fomodoro Header]([https://user-images.githubusercontent.com/.../filename.png](https://github.com/marquisdepolis/fomodoro/blob/main/image.png?raw=true))

# why did i do this?
Because I was procastinating yesterday on doing some tasks on my todo list, and since I didn't already have fomodoro, I ended up spending the time to build it.

It's like what people talk about with AGI. The last invention you'd ever need!

# how to run fomodoro
There are 2 options now
1. On the cloud - you can get a Replicate token, set it in your .env file, and use this
2. On your device - you can download Ollama, run 'ollama run mistral' and 'ollama run llava' to get the models, start your server with 'OLLAMA_HOST=0.0.0.0:11434 ollama serve', and off you go

# what does it do
It takes a screenshot of your screen every 15 minutes, checks against a todo list that exists in the same folder as a txt file, and if you're not on task shows a popup telling you to get back to work.

Simple, easy, and frighteningly effective!

# what's next!
You should build the following, I think
1. Better suggestions on popup - e.g., check the todo list and give actionable feedback or thoughts based on your screen
2. Make the defaults configurable - time limits (15 mins now), default models (mistral and llava now), responses you want to see
3. Run it on demand with a button, including shell if you need to run the Ollama server
4. Run it on someone else's computer so you can tell them to stay on task (this one's for you Elon)
5. Live in a world where productivity increases so fast that by the time the next commit comes we're in utopia!

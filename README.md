# Telegram Bot for Downloading Music from YouTube

This Telegram bot is designed to make it easy and convenient for users to download their favorite music from YouTube links. The bot is built using the Telegram Bot API and can process YouTube links that are sent to it. It utilizes a third-party library to download the audio from the YouTube videos and then sends the downloaded file directly to the user via Telegram. 

## WARNING

Currently not working after YouTube update!!

## Getting Started

To use the bot, simply send a YouTube link to the bot in a private message. The bot will automatically download the audio from the video and send it to you via Telegram. 

## Requirements

To run this app, you need to have `ffmpeg` installed on your system. 

`ffmpeg` is a free and open-source software for handling multimedia data. It is commonly used for processing audio and video files and is required for this app to function properly.

To install `ffmpeg`, follow the instructions for your operating system:

### Windows

Download the latest version of `ffmpeg` from the official website: https://ffmpeg.org/download.html#build-windows

Extract the downloaded zip file to a folder on your computer, then add the `bin` folder to your system's PATH environment variable.

### macOS

Install `ffmpeg` using Homebrew by running the following command in your terminal:

```
brew install ffmpeg
```

### Linux

Install `ffmpeg` using your distribution's package manager. For example, on Ubuntu, run the following command:

```
sudo apt-get install ffmpeg
```

Once `ffmpeg` is installed, you should be able to run the app without any issues.

## Installation

To deploy the bot, follow these steps:

1. Clone the repository to your local machine using Git or download the ZIP file.
2. Create a new bot on Telegram by talking to the BotFather and getting your bot token.
3. Install the required dependencies by running `pip install -r requirements.txt`.
4. Update the `config.py` file with your bot token and other settings as needed.
5. Run the bot using the command `python src/bot.py`.

## Usage

To use the bot, simply send a YouTube link to the bot in a private message. The bot will automatically download the audio from the video and send it to you via Telegram. You can also send a message with a playlist or album link and the bot will download all the songs from that playlist or album.

## Contributing

Contributions to this project are always welcome! If you find a bug or have an idea for a new feature, feel free to submit a pull request or open an issue on the GitHub repository.

When contributing to this project, please make sure to follow the coding standards and use the black code formatter and flake8 linter before submitting any code changes. This will help maintain consistency, readability, and adherence to PEP8 standards throughout the codebase.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.

# Fatawa Processor

## Overview

This repository provides a complete workflow to turn voice recordings into written fatawa and publish to [salafifatawa.org](https://salafifatawa.org).

## What's in the repo

- **audio_downloader**: custom script to do bulk downloads of audio files from website where bulk download option is not available.
                        It requires a custom logic per webpage based on its structure.
- **audio_editor**: provides options to manipulate audio files such as format conversion and trimming.
- **audio_storage**: uploads final audio files to Cloud storage to be referenced by [salafifatawa.org](https://salafifatawa.org).
- **build_mdx**: creates fatawa text in mdx format for easier copy/paste to the website.
- **transcriber**: uses Microsoft Azure speech-to-text service to convert audio files to text.
- **translator**: uses Google translation service to translate Arabic text to English.
- **main**: executes the scripts in a specific order with confirmation at each step.

## Future work

- Add logic to convert audio files from wav to aac after they've been transcribed. This allows for smaller file size
  and for manipulation of the audio controls such as starting at specific time point.
- Refactor scripts to cut audio files into individual fatwa. Each folder would contain a set of individual fatawa
  and each fatwa on the webpage would reference that particular file.
- Obfuscate the workflow and expose it as user-friendly interface behind login page. This would allow for delegating
  the work to other people.
- Add logic to write each fatawa to a database via API calls.
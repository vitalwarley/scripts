# how to

1. Create a virtual environment.
2. Install packages: `pip -r requeriments.txt`
3. Download model:
```
mkdir -p ~/.punctuator
cd ~/.punctuator
gdown https://drive.google.com/uc?id=0B7BsN5f2F1fZd1Q0aXlrUDhDbnM
```
4. Extract and save transcript: `python extract.py --video-id <id> --save-to <filepath>`

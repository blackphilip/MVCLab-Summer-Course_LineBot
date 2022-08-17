# HW - LineBot

## How to run
* **Step 1: Install Python Packages**
    * > pip install -r requirements.txt
* **Step 2: Modifiy `.env.sample` file save as `.env`**
    ```
    LINE_TOKEN = <Line Token>
    LINE_SECRET = <Line Secret Token>
    LINE_UID = <Line UID>
    ```
* **Step 3: Run `calculator_main.py`**
    * > python3 calculator_main.py

* **Info**
   * The port used in calculator_main.py is '2022'.
    

## Commands in LineBot
| Command | Description|
|---|---|
|`<a> + <b>`|Compute a plus b|
|`<a> - <b>`|Compute a minus b|
|`<a> * <b>`|Compute a times b|
|`<a> / <b>`|Compute a divide by b|
|`#help`| Veiew all commands|
|Input any sticker| Return random sticker|

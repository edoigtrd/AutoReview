# AutoReview

This tool is a fun and easy way to generate presentations for your projects.

> This toolwas created for a personnal project aiming to fulfill my laziness. So all the prompts are in french. But you can easily change them. using tools like Google Translate. You can find the prompt in the `prompt.txt` file.

## How to use

First, install the dependencies:

```bash
pip install -r requirements.txt
```

Then, create `config.toml` in the root directory of the project. The file should look like this:

```toml
[keys]
openai="sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
deepai="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

You can get the keys from [OpenAI](https://platform.openai.com/account) and [DeepAI](https://deepai.org/).

Then, you can run the program.
Simply run `main.py` then write a description of your project in natural language. The program will then generate a presentation for you.

## How it works

The program uses GPT-3 to generate the content of the presentation and the HTML code of the presentation.

GPT-3 is asked to generate presentation using tailwindcss and WebSlides.

So, when GPT-3 have generated the body of the presentation, the program will generate the HTML code of the presentation by copying the template.

Once the HTML code is generated, the program will use DeepAI to generate the images of the presentation.

## Example

You can find generated documents as pdf files in the `examples` folder.

The examples are prompted for a project of my first year of computer science school and for [Panoptes](https://github.com/ydhemtek/Panoptes).

## License

This project is licensed under the WTFPL License - see the [LICENSE](LICENSE) file for details

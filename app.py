import io
import os
import subprocess

import click
import dotenv
import openai

dotenv.load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


@click.command()
@click.pass_context
@click.option("--input", type=click.File("rb"))
@click.option("--temperature", default=1, type=float)
def cli(ctx, input, temperature):
    parameters = {
        "input": "",
        "model": "code-davinci-edit-001",
        "n": 1,
        "temperature": temperature,
    }

    code = ""

    if input:
        while True:
            chunk = input.read(1024).decode("utf8")
            if not chunk:
                break
            code += chunk

        if code:
            parameters["input"] = code.strip()

    click.echo(parameters["input"])

    previous_inputs = []

    while True:
        instruction = click.prompt(
            "", default="", show_default=False, prompt_suffix=">>> "
        ).strip()

        # :q quits the application
        if instruction == ":q":
            ctx.exit(-1)

        # If instruction is empty, display input
        if instruction == "":
            click.echo(parameters["input"])
            continue

        # :!, :!python executes the input code in python
        if instruction in [":!", ":!python"]:
            exec(parameters["input"])
            continue

        # :!node, :!js, :!javascript executes the input code in node
        if instruction in [":!node", ":!js", ":!javascript"]:
            p = subprocess.Popen(
                ["node"], stdin=subprocess.PIPE, stdout=subprocess.PIPE
            )
            output = p.communicate(input=parameters["input"].encode("utf8"))
            click.echo(output[0].decode("utf8").strip())
            continue

        # :d deletes the current input setting to ""
        if instruction == ":d":
            parameters["input"] = ""
            click.echo(parameters["input"])
            continue

        # :t followed by a float from 0 to 1 sets the temperature for
        # subsequent API calls
        if instruction.startswith(":t"):
            parameters["temperature"] = float(instruction[2:].lstrip())
            continue

        # :u undoes the last change
        if instruction == ":u":
            if previous_inputs:
                parameters["input"] = previous_inputs.pop(-1)
                click.echo(parameters["input"])
                continue
            click.echo("No undo left")
            continue

        # :w followed by a filename writes the current input to a file
        if instruction.startswith(":w"):
            filename = instruction[2:].strip()
            with open(filename, "wb") as output:
                output.write(parameters["input"].encode("utf8"))
            continue

        if instruction.startswith(":"):
            click.echo("Instruction cannot start with :")
            continue

        parameters["instruction"] = instruction

        response = openai.Edit.create(**parameters)

        # click.echo(response)

        previous_inputs.append(parameters["input"])
        parameters["input"] = response["choices"][0]["text"]
        click.echo(parameters["input"])

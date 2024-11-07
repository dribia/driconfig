# Contribute

<p style="text-align: center; padding-bottom: 1rem;">
    <a href="https://dribia.github.io/driconfig">
        <img
            src="../img/logo_dribia_blau_cropped.png"
            alt="driconfig"
            style="display: block; margin-left: auto; margin-right: auto; width: 40%;"
        >
    </a>
</p>

<p style="text-align: center;">
    <em>Contributions to Dribia libraries are always welcome!</em>
</p>

## Mantainers
DriConfig is maintained by Dribia Data Research <code@dribia.com>.

## Issues
Questions, feature requests and bug reports are all welcome as [discussions or issues](https://github.com/dribia/driconfig/issues).

Please note which version of the library are you using whenever reporting a bug.
```shell
python -c "import driconfig; print(driconfig.__version__)"
```

It would be very useful too to know which OS and Python version are your running DriConfig from.

## Contribute
In order to contribute, the first step is to clone yourself the code:
[repository](https://github.com/dribia/driconfig):
```shell
git clone https://github.com/dribia/driconfig.git
```
Then, you can step into the project's root and, assuming that you have both [Poetry](https://python-poetry.org/) and
[pre-commit](https://pre-commit.com/) installed, run:
```shell
poetry install && pre-commit install
```

Now you should be ready to start coding and prepare your [pull request](https://github.com/dribia/driconfig/pulls).

Remember that you can run linting and tests locally with:

```shell
make lint
make test
```

Happy coding!

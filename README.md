# GnuCash Dashboard

![Screenshot of the GnuCash Dashboard](Screenshot.png)

## Prerequisistes

- [GnuCash](https://gnucash.org/)
- [Python 3](https://www.python.org/)
- [GnuCash Python Bindings](https://wiki.gnucash.org/wiki/Python_Bindings)

### Dependencies

> **Please Note:** The following has been tested on elementary OS 6 (based on Ubuntu 20.04 LTS)

The GnuCash Python Bindings need the GnuCash to be installed from apt. So if you use the GnuCash Flatpak,
make sure to install the GnuCash *.deb package as well:

```bash
sudo apt install gnucash python3-gnucash python3-venv
```

## Start Dashboard

Once the dependencies are installed, navigate to the project root directory and execute the `start.sh` script,
it will install the python dependencies automatically and then run the application:

```bash
./start.sh
```

... your default browser should open at http://127.0.0.1:8050/ and point you at the GnuCash Dashboard.

## Configuration

### Using the `config.py` file

GnuCash Dashboard can be configured by changing the `config.py` file according to your needs. See the config file for further documentation.

### Using Environment Variables

Each variable from the `config.py` file can also be set as Environment Variable using a `GNUCASH2DASH_` prefix. See the `config.py` for
further documentation about the available configuration values as well as their corresponding Environment Variable.

## Testing

GnuCash Dashboard comes with Unit Testing. To execute the tests, simply navigate to the project root directory and execute the `tests.sh`:

```bash
./tests.sh
```
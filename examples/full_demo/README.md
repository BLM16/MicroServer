# Full MicroServer Example

This example application is intended to demonstrate the usage of MicroServer. This example does not follow all good practices for errorhandling, and it is not intended to represent a full-scale application. The purpose is simply to show off the features of MicroServer.

This example server uses PyBars3 to render dynamic Handlebars content since MicroServer does no templating on its own to remain lightweight.

## Files

- The server is registered and started in [main.py](./main.py). The 404 errorhandler is registered here too.

- Routing is all handled in [routes.py](./routes.py) on a `MicroServer.Blueprint` and registered to the server in [main.py](./main.py)

- There is no database for persistent user information, simply an in-memory dictionary. See [auth.py](./auth.py) for the implementation.
    - The `User` class is in [models/user.py](./models/user.py).

- The [.http](./.http) file contains requests that can be made to this example server using the `humao.rest-client` VSCode extension which is automatically installed in the Dev Container.
    - This is not required for MicroServer, this is simply a convenience file for developers.

## Directories

- `/static` contains all the static assets that are requested by path and not dynamic routing (e.g. CSS files).
- `/views` contains all the Handlebars and HTML files that will be rendered for their corresponding routes.
    - `/partials` contains the header file which is registered as a partial for other Handlebars views.

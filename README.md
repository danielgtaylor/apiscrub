# API Scrubber

An OpenAPI scrubber to process and remove certain information depending on the target audience. For example, given something like:

```yaml
paths:
  /hello:
    get:
      description: Returns a hello world string.
  /admin:
    get:
      description: Get the admin settings
      x-only: admin
```

Then running `apiscrub input.yaml -` would result in:

```yaml
paths:
  /hello:
    get:
      description: Returns a hello world string.
```

While running `apiscrub --keep=admin input.yaml -` would result in:

```yaml
paths:
  /hello:
    get:
      description: Returns a hello world string.
  /admin:
    get:
      description: Get the admin settings
```

Note that the `x-only` metadata extension tag gets removed in both cases.

## Installation

Install via Python:

```sh
$ pip install apiscrub
```

## License

Copyright © 2018 Daniel G. Taylor

http://dgt.mit-license.org/

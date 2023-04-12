template
=================

## Setup

Populate `.env` file, use `.env.example`.

Build images:
```
make container@build
```

Start containers:
```
make container@start
```

Prepare dev environment (migrate db, install fixtures, etc.):
```
make project@build-dev
```

Restart containers:
```
make container@restart
```

Log in with credentials `admin / admin`.

## Documentation

Swagger UI available on `/api/docs`.

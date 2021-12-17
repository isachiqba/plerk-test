## Sample Deployment to GCP

```sh
# Create an small VM instance with Container-Optimized OS as the base system.
$ gcloud compute instances create plerk-test \
  ... \
  --machine-type=e2-micro \
  --tags=http-server \
  ...

# SSH into the machine
$ gcloud beta compute ssh plerk-test

# clone the repo
$ git clone https://github.com/isachiqba/plerk-test
$ cd plerk-test
$ ./deploy/docker-compose.sh
```

In this particular case I choose COS as the base operating due its security and lightweight. Unfurtunately I did not foresee the lack of support for the new `docker compose` **cli-plugin** so I manually translate and ran the instructions from `deploy/docker-compose.sh `  using the old `docker-compose` container, e.g.

```sh
`docker compose ...` -> `docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v "$PWD:$PWD" -w="$PWD" docker/compose ...`
```


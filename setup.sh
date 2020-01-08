docker build -t filter --build-arg PORT=6660 --build-arg REGEX="[^0123456789abcdefghijklmnopqrstuvwxyz/= ._']"	--build-arg FLAG="SIG{example_flag}" .
docker run -p 6660:6660 filter

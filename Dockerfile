FROM python:3.9

RUN mkdir -p /var/TrustCalculation

WORKDIR /var/TrustCalculation

COPY ./ /var/TrustCalculation

# Install kubectl from Docker Hub.
COPY --from=lachlanevenson/k8s-kubectl:v1.10.3 /usr/local/bin/kubectl /usr/local/bin/kubectl

RUN pip install -r requirements.txt

ENTRYPOINT python -u /var/TrustCalculation/src/main.py
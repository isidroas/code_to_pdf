FROM danteev/texlive:latest

WORKDIR /workdir

RUN apt-get update
# isolation with python used by latex (e.g pygments)
RUN apt-get install -y python3-venv
RUN python3 -m venv venv
RUN . venv/bin/activate
RUN echo $VIRTUAL_ENV
RUN echo hola $VIRTUAL_ENV
# RUN python -m pip install code_to_pdf
ENV PATH="/workdir/venv/bin:$PATH"
# RUN python -m pip install pipx
COPY . /src
RUN pip install /src/walkfind-0.0.5-py3-none-any.whl
RUN pip install /src/latex-0.7.0.dev1-py3-none-any.whl
RUN pip install -r /src/latex/requirements.txt
WORKDIR /src/latex
RUN python generate.py /src/

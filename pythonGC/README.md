# pythonGC
Para rota os programas dessa pasta é necessário as seguintes dependerias:
- python 3.8
- commonmark
- numpy
- pillow
- pyglm
- pygments
- pyopengl
- pysdl2-dll
- pysdl2
- rich

Para instalar as dependências pode ser usando o pip 
```bash
pip install -r requirements.txt
```

Mas recomendo usar o poetry para instalar as dependências em um ambiente virtual
```bash
poetry install
poetry shell
```

Para executar os programas e necessário executados a partir da pasta raiz do projeto da seguinte forma:
```bash
python pythonGC/GL2Piramide.py

python pythonGC/GL3TexturedQuad.py

python pythonGC/GL3Dado.py

python pythonGC/Gl3Earth.py
```
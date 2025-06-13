# Projeto de analisador de competências

## ✅ Requisitos

- Python 3.6+
- VS Code instalado ([Download](https://code.visualstudio.com/))
- Extensões do VS Code:
  - [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
  - [Jupyter](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter)

---

## ⚙️ Passo a Passo

### 1. Clone ou crie seu projeto
```bash
mkdir meu-projeto
cd meu-projeto
```
### 2.Crie o ambiente virtual
```bash
python3 -m venv .venv
```
### 3.Ative o ambiente virtual
```bash
source .venv/bin/activate
```
### 5. (Opcional) Registre o kernel no Jupyter
```bash
python -m ipykernel install --user --name=jupyter-vscode
```
> Substitua jupyter-vscode por outro nome, se quiser.
### 6. Instale as dependências

```bash
pip install -r requirements.txt
```
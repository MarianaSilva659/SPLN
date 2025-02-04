# TPC 1

## Filtro

- Em python
- O filtro vai fazer:
    - Dado um ficheiro eliminar as linha repetidas
- Dica: 
    - Criar um ficheiro novo com o resultado

#### Solução pela consola

```
awk '!a[$0]++'
```

- Temos de fazer este comando mas em python.
from typing import List

def get_competencias_avaliadas_pipeline(ids_turmas:List):
    """
    Pipeline para obter as competências avaliadas em turmas específicas.
    :param ids_turmas: Lista de IDs das turmas.
    :return: Lista de dicionários representando o pipeline.
    """
    return [
        {
            '$match': {
                'turma': {
                    '$in': ids_turmas
                }
            }
        }, {
            '$unwind': {
                'path': '$grafos'
            }
        }, {
            '$unwind': {
                'path': '$grafos.arestas'
            }
        }, {
            '$set': {
                'grafos.arestas.valor': {
                    '$avg': '$grafos.arestas.valor'
                }
            }
        }, {
            '$group': {
                '_id': '$grafos.competencia',
                'seriesAvaliadas': {
                    '$push': '$grafos.arestas.origem.serie_ano'
                },
                'arestas': {
                    '$push': '$grafos.arestas'
                }
            }
        }, {
            '$set': {
                'numDisplAval.ano1': {
                    '$size': {
                        '$filter': {
                            'input': '$seriesAvaliadas',
                            'as': 'nota',
                            'cond': {
                                '$eq': [
                                    '$$nota', 1
                                ]
                            }
                        }
                    }
                },
                'numDisplAval.ano2': {
                    '$size': {
                        '$filter': {
                            'input': '$seriesAvaliadas',
                            'as': 'nota',
                            'cond': {
                                '$eq': [
                                    '$$nota', 2
                                ]
                            }
                        }
                    }
                },
                'numDisplAval.ano3': {
                    '$size': {
                        '$filter': {
                            'input': '$seriesAvaliadas',
                            'as': 'nota',
                            'cond': {
                                '$eq': [
                                    '$$nota', 3
                                ]
                            }
                        }
                    }
                }
            }
        }, {
            '$project': {
                'seriesAvaliadas': 0
            }
        }, {
            '$addFields': {
                'sumValorCompetencias': {
                    '$sum': '$arestas.valor'
                }
            }
        }, {
            '$set': {
                '_id': {
                    '$toObjectId': '$_id'
                }
            }
        }, {
            '$lookup': {
                'from': 'competencias',
                'localField': '_id',
                'foreignField': '_id',
                'as': 'competencia_details'
            }
        }, {
            '$set': {
                'competencia_details': {
                    '$first': '$competencia_details'
                }
            }
        }, {
            '$set': {
                'competencia_tag': '$competencia_details.tag'
            }
        }, {
            '$project': {
                'competencia_details': 0,
            }
        }, {
            '$set': {
                '_id': {
                    '$toString': '$_id'
                }
            }
        }
    ]

def get_turmas_do_aluno_pipeline(nome_escola:str, nome_aluno:str):
    """
    Pipeline para obter as turmas de um aluno específico em uma escola.
    :param nome_escola: Nome da escola.
    :param nome_aluno: Nome do aluno.
    :return: Lista de dicionários representando o pipeline.
    """
    return [
        {
          '$match': {
              'nome': nome_escola
          }
        },
        {
          "$unwind": "$turmas"
        },
        {
          "$unwind": "$turmas.alunos"
        },
        {
          "$project": {
            "_id": 0,
            "turmas": 1
          }
        },
        {
          "$replaceRoot":  { "newRoot": "$turmas" }
        },
        {
          "$match": {
            "alunos.nome": nome_aluno
            }
        },
        {
          "$project": {
            "alunos.idade": 0
          }
        },
        {
          "$set": {
              "aluno": "$alunos"
          }
        },
        {
          "$unset": "alunos"
        },
        {
          "$set":{
              "aluno.notas.historico_escolar": {
                  "$map":{
                      "input": "$aluno.notas.historico_escolar",
                      "as": "item",
                      "in": {
                          "disciplina_id": {"$toString":"$$item._id"},
                          "nota": "$$item.nota",
                          "disciplina_titulo": "$$item.disciplina_titulo"
                      }
                  }
              }
          }
        },
        {
            "$set": {
                "_id": {
                    "$toString": "$_id"
                }
            }
        },
        {
            '$sort': {
                'aluno.serie': 1
            }
        }
    ]



def get_arestas_total_pipeline():
    """
    Pipeline para obter as arestas totais de todas as turmas.
    :return: Lista de dicionários representando o pipeline.
    """
    return [
    {
        '$unwind': '$grafos'
    }, {
        '$project': {
            'totalArestas': {
                '$size': '$grafos.arestas'
            }
        }
    }, {
        '$group': {
            '_id': None, 
            'totalArestasGeral': {
                '$sum': '$totalArestas'
            }
        }
    }
]

def get_disciplina_por_area_pipeline():
    return [ 
        {
            '$set': {
                'numDiscip.LINGUAGENS': {
                    '$size': {
                        '$filter': {
                            'input': '$disciplinas', 
                            'as': 'disciplina', 
                            'cond': {
                                '$eq': [
                                    '$$disciplina.area', 'LINGUAGENS'
                                ]
                            }
                        }
                    }
                }, 
                'numDiscip.EXATAS': {
                    '$size': {
                        '$filter': {
                            'input': '$disciplinas', 
                            'as': 'disciplina', 
                            'cond': {
                                '$eq': [
                                    '$$disciplina.area', 'EXATAS'
                                ]
                            }
                        }
                    }
                }, 
                'numDiscip.HUMANAS': {
                    '$size': {
                        '$filter': {
                            'input': '$disciplinas', 
                            'as': 'disciplina', 
                            'cond': {
                                '$eq': [
                                    '$$disciplina.area', 'HUMANAS'
                                ]
                            }
                        }
                    }
                }, 
                'numDiscip.NATUREZA': {
                    '$size': {
                        '$filter': {
                            'input': '$disciplinas', 
                            'as': 'disciplina', 
                            'cond': {
                                '$eq': [
                                    '$$disciplina.area', 'NATUREZA'
                                ]
                            }
                        }
                    }
                }
            }
        }, {
            '$project': {
                '_id': 1, 
                'numDiscip': 1
            }
        }
    ]

def get_competencia_por_area_pipeline():
    return [
        {
        '$group': {
            '_id': '$tag', 
            'total': {
                '$sum': 1
            }
        }
        }, {
            '$project': {
                '_id': 0, 
                'tipo': '$_id', 
                'total': 1
            }
        }, {
            '$sort': {
                'total': -1
            }
        }
    ]

def get_legendas_colunas_pipeline():
    return [
        {
            '$addFields': {
                'code': {
                    '$cond': {
                        'if': {
                            '$ne': [
                                '$tag', 'COGNITIVOS'
                            ]
                        },
                        'then': {
                            '$map': {
                                'input': {
                                    '$objectToArray': '$competencias_habilidades'
                                },
                                'as': 'item',
                                'in': '$$item.k'
                            }
                        },
                        'else': {
                            '$map': {
                                'input': {
                                    '$split': [
                                        '$nome', ' '
                                    ]
                                },
                                'as': 'palavra',
                                'in': {
                                    '$substrCP': [
                                        '$$palavra', 0, 1
                                    ]
                                }
                            }
                        }
                    }
                }
            }
        }, {
            '$set': {
                'code': {
                    '$concat': [
                        {
                            '$substrCP': [
                                '$tag', 0, 3
                            ]
                        }, '.', {
                            '$first': '$code'
                        }, '.', {
                            '$toUpper': {
                                '$last': '$code'
                            }
                        }
                    ]
                }
            }
        }, {
            '$group': {
                '_id': None,
                'documentosUnificados': {
                    '$mergeObjects': {
                        '$arrayToObject': [
                            {
                                '$map': {
                                    'input': {
                                        '$objectToArray': '$$ROOT'
                                    },
                                    'as': 'doc',
                                    'in': {
                                        'k': {
                                            '$toString': '$_id'
                                        },
                                        'v': {
                                            'area': '$tag',
                                            'codigo': '$code'
                                        }
                                    }
                                }
                            }
                        ]
                    }
                }
            }
        }, {
            '$replaceRoot': {
                'newRoot': '$documentosUnificados'
            }
        }
    ]

import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt

# É necessário instalar o pacote jinja2 (pip install jinja2)
def df_summary_report(df):
    """
    Descreve valores estatísticos da dataframe.

    Parâmetros
    ----------
    df : pd.DataFrame
        DataFrame a ser analisado.
    Retorno
    -------
    pd.Series
        Valores estatísticos e quantitativos estilizados.
    """

    moda = df.mode().iloc[0]

    mem_consumo = df.memory_usage(deep=True, index=False)/1024**2
    total = sum(mem_consumo)

    freq = df.apply(
        lambda col: col.value_counts(dropna=True).iloc[0]
        if not col.dropna().empty else None
    )


    resumo = pd.DataFrame({
        'Coluna': df.columns,            #Lista os nomes das colunas do DataFrame.
        'Tipo': df.dtypes.values,        #Retorna o tipo de dado (dtype) de cada coluna.
        'Quantidade de Dados Não Vazios': df.notna().sum().values,  #Conta a quantidade de valores não nulos por coluna.
        'Quantidade de Dados Vazios': df.isna().sum().values,       #Conta a quantidade de valores nulos (NaN) por coluna.
        'Valores Únicos': df.nunique().values,       #Conta a quantidade de valores únicos de cada coluna
        'Valor mais Frequente': moda,    #Calcula a moda de cada coluna    
        'Frequência': freq,               #Mostra a frequência da moda
        'Porcentagem de Unicidade': ((df.nunique() / len(df)) * 100).round(2).values,    #Cardinalidade - baixa cardinalidade indica alta repetição; alta cardinalidade indica baixa repetição
        'Porcentagem de Valor Vazios (%)': (df.isna().mean() * 100).round(2).values,  #Calcula a porcentagem de valores nulos por coluna.
        f'Consumo de Memória - Total: {total:.2f} (MB)': mem_consumo
    }).reset_index(drop=True)

    #colormaps
    cmap_vazios = sns.light_palette("#BD2A2E", as_cmap=True)
    cmap_unicidade = sns.light_palette("#13678A", as_cmap=True)
    cmap_unique = sns.light_palette("#1f77b4", as_cmap=True)
    cmap_freq = sns.light_palette("#13678A", as_cmap=True)

    styled = (resumo.style
        .set_properties(**{
            'background-color': "#101719",
            'color': '#E0E0E0',  
            'border': '1px solid #2F3D40',
            'text-align': 'center'
        })
        .background_gradient(subset=['Porcentagem de Valor Vazios (%)'], cmap=cmap_vazios, vmin=0, vmax=100)
        .background_gradient(subset=['Porcentagem de Unicidade'], cmap=cmap_unicidade, vmin=0, vmax=100)
        .background_gradient(subset=["Valores Únicos"],cmap=cmap_unique)
        .background_gradient(subset=["Frequência"],cmap=cmap_freq)
        .background_gradient(subset=[f"Consumo de Memória - Total: {total:.2f} (MB)"], cmap=cmap_freq)
        .bar(subset=['Quantidade de Dados Vazios'], color="#BD2A2E")
        .format({'Porcentagem de Valor Vazios (%)': '{:.2f}', 'Porcentagem de Unicidade': '{:.2f}'})
        .set_table_styles([{
                'selector': 'th',
                'props': [
                    ('background-color', "#0c2845"),
                    ('color', 'white'),
                    ('text-align', 'center'),
                    ('font-size', '13px')
                ]
            }
        ])
        .set_properties(
            subset=pd.IndexSlice[:, resumo.columns[0]],**{
                'background-color': '#012030',
                'font-weight': 'bold',
                'color': '#FFFFFF'
            })
        
    )
    return styled
#----------------------------------------------------------------------------------------------------------------------
def plot_categorical_distributions(df, palette):
    """
    Plota a distribuição das principais variáveis categóricas do conjunto de dados.

    A função gera três gráficos de contagem (countplot) para visualizar
    a frequência das categorias presentes nas colunas:

    - TransactionType: tipo de transação (crédito ou débito);
    - Channel: canal utilizado para realizar a transação;
    - CustomerOccupation: profissão do cliente.
    """

    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(15, 5))

    sns.countplot(x='TransactionType', data=df, palette=palette, ax=axes[0])
    axes[0].set_title('Comparação entre Tipos de Transação')
    axes[0].set_xlabel('Tipo de Transação (Credit/Debit)')
    axes[0].set_ylabel('Quantidade')
    axes[0].set_axisbelow(True)
    axes[0].grid(axis='y', color='gray', linestyle='--', linewidth=0.7)
    sns.despine(left=True, bottom=True)


    sns.countplot(x="Channel", data=df, palette=palette, ax=axes[1])
    axes[1].set_title("Comparação entre os Tipos de Canal")
    axes[1].set_xlabel("Canal de Acesso")
    axes[1].set_ylabel('Quantidade')
    axes[1].set_axisbelow(True)
    axes[1].grid(axis='y', color='gray', linestyle='--', linewidth=0.7)
    sns.despine(left=True, bottom=True)


    sns.countplot(x="CustomerOccupation", data=df, palette=palette, ax=axes[2])
    axes[2].set_title("Comparação entre as Profissões dos Clientes")
    axes[2].set_xlabel("Profissão")
    axes[2].set_ylabel('Quantidade')
    axes[2].set_axisbelow(True)
    axes[2].grid(axis='y', color='gray', linestyle='--', linewidth=0.7)
    sns.despine(left=True, bottom=True)

    plt.tight_layout()
    plt.show()
#-------------------------------------------------------------------------------------------------------
def plot_financial_distributions(df, palette):
    """
    Analisa a distribuição das principais variáveis financeiras do dataset.

    A função gera visualizações para explorar o comportamento dos dados
    relacionados às transações e ao saldo das contas, incluindo:

    - Distribuição dos valores das transações (TransactionAmount);
    - Distribuição dos saldos das contas (AccountBalance);
    - Saldo médio das contas por profissão do cliente (CustomerOccupation).
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    sns.histplot(df['TransactionAmount'], bins=20, kde=True, color="#3B3936", ax=axes[0])
    axes[0].set_title('Distribuição dos Valores das Transações')
    axes[0].set_xlabel('Valor das Transações')
    axes[0].set_ylabel('Frequência')

    sns.histplot(df['AccountBalance'], bins=10, kde=False, color="#3B3936", ax=axes[1])
    axes[1].set_title('Distribuição do Saldo nas Contas')
    axes[1].set_xlabel('Saldo da Conta')
    axes[1].set_ylabel('Frequência')

    prof_valor_conta = df.groupby("CustomerOccupation")["AccountBalance"].mean()
    sns.barplot(x=prof_valor_conta.index, y=prof_valor_conta.values, palette=palette, ax=axes[2])
    axes[2].set_title(f'Média dos Valores na Conta')
    axes[2].set_xlabel("Profissão")
    axes[2].set_ylabel('Média')
    axes[2].set_axisbelow(True)
    axes[2].grid(axis='y', color='gray', linestyle='--', linewidth=0.7)
    sns.despine(left=True, bottom=True)

    plt.tight_layout()
    plt.show()
#----------------------------------------------------------------------------------------------
def analyze_customer_behavior(df):
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    sns.histplot(df['TransactionDuration'], bins=20, kde=True, color="#3B3936", ax=axes[0])
    axes[0].set_title('Distribuição da Duração das Transações')
    axes[0].set_xlabel('Duração das Transações (segundos)')
    axes[0].set_ylabel('Frequência')

    sns.histplot(df['LoginAttempts'], bins=5, kde=False, color="#3B3936", ax=axes[1]) 
    axes[1].set_title('Distribuição das Tentativas de Login')
    axes[1].set_xlabel('Tentativa de Login')
    axes[1].set_ylabel('Frequência')

    sns.histplot(df['CustomerAge'], bins=20, kde=True, color="#3B3936", ax=axes[2])
    axes[2].set_title('Distribuição da Idade dos Clientes')
    axes[2].set_xlabel('Idade dos Clientes')
    axes[2].set_ylabel('Frequência')

    plt.tight_layout()
    plt.show()
#--------------------------------------------------------------------------------------------------------
def mean_transaction(df, palette):
    """
    Analisa o valor médio das transações em diferentes segmentos do dataset.

    A função calcula e exibe a média dos valores de transação
    (TransactionAmount) agrupados por:

    - Profissão do cliente (CustomerOccupation);
    - Canal de acesso utilizado na transação (Channel);
    - Tipo de transação (TransactionType).
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    prof_valor = df.groupby("CustomerOccupation")["TransactionAmount"].mean()
    sns.barplot(x=prof_valor.index, y=prof_valor.values, palette=palette, ax=axes[0])
    axes[0].set_title(f'Média dos Valores de Transação por Profissão')
    axes[0].set_xlabel("Profissão")
    axes[0].set_ylabel('Média')
    axes[0].set_axisbelow(True)
    axes[0].grid(axis='y', color='gray', linestyle='--', linewidth=0.7)
    sns.despine(left=True, bottom=True)

    canal_valor = df.groupby("Channel")["TransactionAmount"].mean()
    sns.barplot(x=canal_valor.index, y=canal_valor.values, palette=palette, ax=axes[1])
    axes[1].set_title(f'Média dos Valores de Transação por Canal de Acesso')
    axes[1].set_xlabel("Tipo de Canal de Acesso")
    axes[1].set_ylabel('Média')
    axes[1].set_axisbelow(True)
    axes[1].grid(axis='y', color='gray', linestyle='--', linewidth=0.7)
    sns.despine(left=True, bottom=True)

    trans_valor = df.groupby("TransactionType")["TransactionAmount"].mean()
    sns.barplot(x=trans_valor.index, y=trans_valor.values, palette=palette, ax=axes[2])
    axes[2].set_title(f'Média dos Valores de Transação por Tipo')
    axes[2].set_xlabel("Tipo de Transação")
    axes[2].set_ylabel('Média')
    axes[2].set_axisbelow(True)
    axes[2].grid(axis='y', color='gray', linestyle='--', linewidth=0.7)
    sns.despine(left=True, bottom=True)

    plt.tight_layout()
    plt.show()
#------------------------------------------------------------------------------------------------
def plot_loggin_attempts(df, palette):
    """
    Mostra a quantidade de tentativa que os clientes realizam quando vão logar em 
    suas contas e o tipo de operação.

    A função calcula a quantidade de tentativas por tipo de transação:

    - Tentativa de Login (LoginAttempts);
    - Tipo de transação (TransactionType)
    """
    contagem = df.groupby("LoginAttempts")["TransactionType"].value_counts().unstack()

    plt.figure(figsize=(12, 4))

    ax = contagem.plot(kind='bar', figsize=(12, 4), color=palette)

    plt.title('Contagem de Tentativas de Login por Tipo de Transação')
    plt.xlabel('Número de Tentativas de Login')
    plt.xticks(rotation=0)
    plt.ylabel('Contagem')
    plt.grid(axis='y', linestyle='--', linewidth=0.7)
    plt.legend(title='Tipo de Transação')

    for p in ax.patches:
        ax.annotate(
            int(p.get_height()),
            (p.get_x() + p.get_width()/2, p.get_height()),
            ha='center',
            va='bottom',
            fontsize=10
        )

    plt.tight_layout()
    plt.show()
#--------------------------------------------------------------------------------------------------
def transactions_over_time(df):
    """
    Gera um gráfico de linha mostrando a contagem diária de transações.

    O DataFrame é agrupado pela coluna 'TransactionDate', contabilizando
    o número de transações realizadas em cada dia. Em seguida, é exibido
    um gráfico de linha para facilitar a análise da evolução temporal 
    das transações.
    """
    # Agrupe por data e conte as transações
    daily_transactions = df.groupby(df['TransactionDate'].dt.date).size().reset_index(name='TransactionCount')
    daily_transactions['TransactionDate'] = pd.to_datetime(daily_transactions['TransactionDate'])

    plt.figure(figsize=(15, 6))  
    sns.lineplot(x='TransactionDate', y='TransactionCount', data=daily_transactions, color="#FFA500")
    plt.title('Contagem Diária de Transações')
    plt.xlabel('Data')
    plt.ylabel('Número de Transações')
    plt.grid(True)
    plt.tight_layout()  
    plt.show()

#---------------------------------------------------------------------------------------------------
def plot_transaction(df, palette):
    """
    Exibe a distribuição das transações por dia da semana e meses do ano.

    A função extrai o dia da semana e meses do ano a partir da 
    coluna 'TransactionDate', contabiliza a quantidade de transações
    realizadas e gera um gráfico de barras para visualizar essa distribuição.

    """
    # Extrai o dia da semana
    df['Day_of_Week'] = df['TransactionDate'].dt.day_name()
    # Extrai o mês do ano
    df['Mes'] = df['TransactionDate'].dt.month_name()

    #Agrupa por dia da semana e conte as transações.
    weekday_counts = df['Day_of_Week'].value_counts().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    #Agrupa por mes e conte as transações.
    mes_counts = df['Mes'].value_counts().reindex(["January", "February", "March", "April", "May", "June", 
                                                    "July", "August", "September", "October", "November", "December"])

    fig, axes = plt.subplots(2, 1, figsize=(15, 7))

    sns.barplot(x=weekday_counts.index, y=weekday_counts.values, palette=palette[::-1], ax=axes[0])
    axes[0].set_title('Contagem de Transações por Dia da Semana')
    axes[0].set_xlabel('Dia da Semana')
    axes[0].set_ylabel('Número de Transações')
    axes[0].grid(axis='y', linestyle='--')

    sns.barplot(x=mes_counts.index, y=mes_counts.values, palette=palette, ax=axes[1])
    axes[1].set_title('Contagem de Transações por Mês')
    axes[1].set_xlabel('Meses do Ano')
    axes[1].set_ylabel('Número de Transações')
    axes[1].grid(axis='y', linestyle='--')

    plt.tight_layout()
    plt.show()
#-------------------------------------------------------------------------------------------------------
def plot_atypical_transaction(data, palette):
    """
    Exibe a distribuição das transações realizadas em horários atípicos
    ao longo dos dias da semana e meses do ano.

    A função gera um gráfico de barras mostrando a quantidade de
    transações registradas em cada dia da semana e mês para um conjunto
    de dados previamente filtrado contendo apenas transações
    consideradas atípicas.

    """
    # Extrai o dia da semana
    data['Day_of_Week'] = data['TransactionDate'].dt.day_name()
    # Extrai os meses do ano
    data['Mes'] = data['TransactionDate'].dt.month_name()

    #Agrupa por dia da semana e conte as transações.
    weekday_counts = data['Day_of_Week'].value_counts().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

    #Agrupa por dia da semana e conte as transações.
    mes_counts = data['Mes'].value_counts().reindex(["January", "February", "March", "April", "May", "June", 
                                                                    "July", "August", "September", "October", "November", "December"])

    
    fig, axes = plt.subplots(2, 1, figsize=(15, 8))

    sns.barplot(x=weekday_counts.index, y=weekday_counts.values, palette=palette[::-1], ax=axes[0])
    axes[0].set_title('Transações em Horários Atípicos por Dia da Semana')
    axes[0].set_xlabel('Dia da Semana')
    axes[0].set_ylabel('Quantidade')
    axes[0].grid(axis='y', linestyle='--')

    sns.barplot(x=mes_counts.index, y=mes_counts.values, palette=palette, ax=axes[1])
    axes[1].set_title('Transações em Horários Atípicos por Mês')
    axes[1].set_xlabel('Meses do Ano')
    axes[1].set_ylabel('Quantidade')
    axes[1].grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout() 
    plt.show()

#------------------------------------------------------------------------------------------------

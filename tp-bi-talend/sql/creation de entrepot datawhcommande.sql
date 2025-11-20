CREATE DATABASE DataWHCommande;
GO

CREATE TABLE Dim_Client (
    id_seqClient INT NOT NULL,
    id_client_prod INT,
    source_prod VARCHAR(50),
    CompanyName VARCHAR(100),
    City VARCHAR(50),
    Country VARCHAR(50)
);
GO

CREATE TABLE Dim_Employee (
    id_seqEmployee INT NOT NULL,
    id_employee_prod INT,
    source_prod VARCHAR(50),
    Nom VARCHAR(50),
    Prenom VARCHAR(50),
    Territory VARCHAR(50),
    TerritoryDescr VARCHAR(100),
    Region VARCHAR(50)
);
GO

CREATE TABLE Dim_Temps (
    id_temps INT NOT NULL,
    annee INT,
    mois_annee VARCHAR(7)
);
GO

CREATE TABLE TF_Commande (
    id_seq_fait INT NOT NULL,
    id_temps INT NOT NULL,
    id_seqEmployee INT NOT NULL,
    id_seqClient INT NOT NULL,
    nb_commandes_livrees INT,
    nb_commandes_non_livrees INT
);
GO

ALTER TABLE Dim_Client
ADD CONSTRAINT pk_Dim_Client PRIMARY KEY (id_seqClient);
GO

ALTER TABLE Dim_Employee
ADD CONSTRAINT pk_Dim_Employee PRIMARY KEY (id_seqEmployee);
GO

ALTER TABLE Dim_Temps
ADD CONSTRAINT pk_Dim_Temps PRIMARY KEY (id_temps);
GO

ALTER TABLE TF_Commande
ADD
    CONSTRAINT fk_TF_Commande_Dim_Client FOREIGN KEY (id_seqClient) REFERENCES Dim_Client(id_seqClient),
    CONSTRAINT fk_TF_Commande_Dim_Employee FOREIGN KEY (id_seqEmployee) REFERENCES Dim_Employee(id_seqEmployee),
    CONSTRAINT fk_TF_Commande_Dim_Temps FOREIGN KEY (id_temps) REFERENCES Dim_Temps(id_temps),
    CONSTRAINT pk_TF_Commande PRIMARY KEY (id_seq_fait, id_seqClient, id_seqEmployee, id_temps);
GO
create table if not exists StockPrice (
    id serial primary key,
    indexId varchar(20) NOT NULL,
    chartOpen numeric NOT NULL,
    chartClose numeric NOT NULL,
    chartLow numeric NOT NULL,
    chartHigh numeric NOT NULL,
    totalQtty bigint NOT NULL,
    totalValue bigint NOT NULL,
    dateTime timestamp NOT NULL
);

create table if not exists StockPriceHour (
    id serial primary key,
    indexId varchar(20) NOT NULL,
    chartOpen numeric NOT NULL,
    chartClose numeric NOT NULL,
    chartLow numeric NOT NULL,
    chartHigh numeric NOT NULL,
    totalQtty bigint NOT NULL,
    totalValue bigint NOT NULL,
    dateTime timestamp NOT NULL
)
FROM mcr.microsoft.com/dotnet/sdk:5.0 AS build
WORKDIR /src
COPY ["csharpfn.csproj", "."]
RUN dotnet restore "csharpfn.csproj"
COPY . .
RUN dotnet build "csharpfn.csproj" -c Release -o /app

FROM build AS publish
RUN dotnet publish "csharpfn.csproj" -c Release -o /app

FROM oraclelinux:7-slim

RUN  rpm -Uvh https://packages.microsoft.com/config/centos/7/packages-microsoft-prod.rpm && \ 
     yum -y install dotnet-sdk-5.0 && \
     rm -rf /var/cache/yum && \
     groupadd --gid 1000 fn && \
     adduser --uid 1000 --gid fn fn

WORKDIR /app
COPY --from=publish /app .
ENTRYPOINT ["dotnet", "csharpfn.dll"]
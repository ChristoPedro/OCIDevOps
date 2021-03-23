FROM microsoft/dotnet:2.2-aspnetcore-runtime AS base
WORKDIR /app

FROM microsoft/dotnet:2.2-sdk AS build
WORKDIR /src
COPY ["csharpfn.csproj", "."]
RUN dotnet restore "csharpfn.csproj"
COPY . .
RUN dotnet build "csharpfn.csproj" -c Release -o /app

FROM build AS publish
RUN dotnet publish "csharpfn.csproj" -c Release -o /app

FROM base AS final
WORKDIR /app
COPY --from=publish /app .
ENTRYPOINT ["dotnet", "csharpfn.dll"]
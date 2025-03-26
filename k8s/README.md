
```Starts the projet : ```

1 - Install OrbStack (https://orbstack.dev/) or Init Kubernetes from Docker Desktop

2 - Go to project root (not in /app)

3 - Run the project : helm upgrade --install app ./app -n app

4 - Create Config map (if needed) : kubectl create configmap app-postgres-init-script --from-file=init.sql -n app

5 - Delete the pods from its namespace : kubectl delete deployments,statefulsets,daemonsets --all -n app

Note : Careful about the SQL data. It is not dynamic. 


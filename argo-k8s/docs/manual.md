# Install argocd
```bash
brew install argocd
```

# Create cluster
```bash
k3d cluster delete argodevops
k3d cluster create argodevops --api-port 6550 -p "8081:80@loadbalancer"

export KUBECONFIG="$(k3d kubeconfig write argodevops)"
```

## Adiciona nodes
```bash
k3d node create argodevops-node -c argodevops  --replicas 3
```

# #Instala a stack de monitoracao do lens
```bash
kubectl apply -f argo-k8s/files/lens-metric/01-namespace.yml
kubectl apply -f argo-k8s/files/lens-metric/02-configmap.yml
kubectl apply -f argo-k8s/files/lens-metric/02-service-account.yml
kubectl apply -f argo-k8s/files/lens-metric/03-service.yml
kubectl apply -f argo-k8s/files/lens-metric/03-statefulset.yml
kubectl apply -f argo-k8s/files/lens-metric/04-rules.yml
kubectl apply -f argo-k8s/files/lens-metric/05-clusterrole.yml
kubectl apply -f argo-k8s/files/lens-metric/06-clusterrole-binding.yml
kubectl apply -f argo-k8s/files/lens-metric/10-node-exporter-ds.yml
kubectl apply -f argo-k8s/files/lens-metric/11-node-exporter-svc.yml
kubectl apply -f argo-k8s/files/lens-metric/12-kube-state-metrics-clusterrole.yml
kubectl apply -f argo-k8s/files/lens-metric/12.kube-state-metrics-sa.yml
kubectl apply -f argo-k8s/files/lens-metric/13-kube-state-metrics-clusterrole-binding.yml
kubectl apply -f argo-k8s/files/lens-metric/14-kube-state-metrics-deployment.yml
kubectl apply -f argo-k8s/files/lens-metric/14-kube-state-metrics-svc.yml 

# Adiciona o argocd no cluster kubernetes
```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

## Inclui o --insecure para o ArgoCD funcionar via ingress Traefik
```bash
kubectl patch deployments argocd-server -n argocd -p '{"spec":{"template":{"spec": {"containers":[{"name":"argocd-server","command":[ "argocd-server", "'--staticassets'", "/shared/app", "'--insecure'"]}]}}}}' 
```

# Cria os ingress para acesso via hostname
```bash
kubectl apply -f argo-k8s/files/ingress/argocd.yaml 
kubectl apply -f argo-k8s/files/ingress/prometheus.yaml 
```

# Para mudar o hostname sem localhost
# sudo $(which hostess) add argocd.argodevops.com 127.0.0.1
# sudo $(which hostess) add prometheus.argodevops.com 127.0.0.1
# Editar os arquivos ingress para apontar para *.argodevops.com em vez de *.argodevops.localhost

```bash
echo "ArcoCD: http://argocd.argodevops.localhost:8081"
echo "ArcoCD admin username: admin"
echo "ArcoCD admin password: $(kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d)"
echo "Prometheus: http://prometheus.argodevops.localhost:8081"

```
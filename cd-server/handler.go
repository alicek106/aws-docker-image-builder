/* Author : alicek106
*  Date : 2019. 06. 25
*/
// Reference : https://github.com/kubernetes/client-go/tree/master/examples/create-update-delete-deployment

package main

import (
	"fmt"
	apiv1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/rest"
	"k8s.io/client-go/util/retry"
)

type Updator struct{
	K8sEndpoint string
}

func (u* Updator) UpdateDeploymentImage (deploymentName string, newImageName string) {
	config, err := rest.InClusterConfig()
	if err != nil {
		panic(err.Error())
	}
	var clientset, _ = kubernetes.NewForConfig(config)

	if err != nil {
		panic(err.Error())
	}

	deploymentsClient := clientset.AppsV1().Deployments(apiv1.NamespaceDefault)

	fmt.Println("Updating deployment...")
	retryErr := retry.RetryOnConflict(retry.DefaultRetry, func() error {
		result, getErr := deploymentsClient.Get(deploymentName, metav1.GetOptions{})
		if getErr != nil {
			panic(fmt.Errorf("Failed to get latest version of Deployment: %v", getErr))
		}

		result.Spec.Template.Spec.Containers[0].Image = newImageName
		_, updateErr := deploymentsClient.Update(result)
		return updateErr
	})
	if retryErr != nil {
		panic(fmt.Errorf("Update failed: %v", retryErr))
	}
	fmt.Println("Updated deployment...")
}
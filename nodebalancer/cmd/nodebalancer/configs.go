/*
Configurations for load balancer server.
*/
package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"path/filepath"
	"strconv"
	"strings"
	"time"

	bugout "github.com/bugout-dev/bugout-go/pkg"
	"github.com/google/uuid"
)

var (
	nodeConfigs []NodeConfig

	supportedBlockchains map[string]bool

	bugoutClient *bugout.BugoutClient

	// Bugout client
	// TODO(kompotkot): Find out why it cuts out the port
	BUGOUT_BROOD_URL = "https://auth.bugout.dev"
	// BUGOUT_BROOD_URL              = os.Getenv("BUGOUT_BROOD_URL")
	NB_BUGOUT_TIMEOUT_SECONDS_RAW = os.Getenv("NB_BUGOUT_TIMEOUT_SECONDS")

	// Bugout and application configuration
	BUGOUT_AUTH_CALL_TIMEOUT        = time.Second * 5
	MOONSTREAM_APPLICATION_ID       = os.Getenv("MOONSTREAM_APPLICATION_ID")
	NB_CONTROLLER_USER_ID           = os.Getenv("NB_CONTROLLER_USER_ID")
	NB_CONTROLLER_TOKEN             = os.Getenv("NB_CONTROLLER_TOKEN")
	NB_CONTROLLER_ACCESS_ID         = os.Getenv("NB_CONTROLLER_ACCESS_ID")
	MOONSTREAM_CORS_ALLOWED_ORIGINS = os.Getenv("MOONSTREAM_CORS_ALLOWED_ORIGINS")
	CORS_WHITELIST_MAP              = make(map[string]bool)

	NB_ENABLE_DEBUG = false

	NB_CONNECTION_RETRIES          = 2
	NB_CONNECTION_RETRIES_INTERVAL = time.Second * 5
	NB_HEALTH_CHECK_INTERVAL       = 30
	NB_HEALTH_CHECK_INTERVAL_RAW   = os.Getenv("NB_HEALTH_CHECK_INTERVAL")
	NB_HEALTH_CHECK_CALL_TIMEOUT   = time.Second * 2

	NB_CACHE_CLEANING_INTERVAL              = 10
	NB_CACHE_CLEANING_INTERVAL_RAW          = os.Getenv("NB_CACHE_CLEANING_INTERVAL")
	NB_CACHE_ACCESS_ID_LIFETIME             = int64(120) // After 2 minutes, the access ID will be deleted from the cache if there has been no activity
	NB_CACHE_ACCESS_ID_LIFETIME_RAW         = os.Getenv("NB_CACHE_ACCESS_ID_LIFETIME")
	NB_CACHE_ACCESS_ID_SESSION_LIFETIME     = int64(900) // After 15 minutes, the access ID will be deleted from the cache to refresh access limits
	NB_CACHE_ACCESS_ID_SESSION_LIFETIME_RAW = os.Getenv("NB_CACHE_ACCESS_ID_SESSION_LIFETIME")

	NB_MAX_COUNTER_NUMBER = uint64(10000000)

	// Client configuration
	NB_CLIENT_NODE_KEEP_ALIVE = int64(5) // How long to store node in hot list for client in seconds

	NB_ACCESS_ID_HEADER   = os.Getenv("NB_ACCESS_ID_HEADER")
	NB_DATA_SOURCE_HEADER = os.Getenv("NB_DATA_SOURCE_HEADER")

	// Humbug configuration
	HUMBUG_REPORTER_NB_TOKEN = os.Getenv("HUMBUG_REPORTER_NB_TOKEN")

	// Moonstream resources types
	BUGOUT_RESOURCE_TYPE_NODEBALANCER_ACCESS   = "nodebalancer-access"
	DEFAULT_AUTOGENERATED_USER_PERMISSIONS     = []string{"read"}
	DEFAULT_AUTOGENERATED_PERIOD_DURATION      = int64(86400)
	DEFAULT_AUTOGENERATED_MAX_CALLS_PER_PERIOD = int64(1000)
)

func CreateBugoutClient() (*bugout.BugoutClient, error) {
	bugoutTimeoutSeconds, err := strconv.Atoi(NB_BUGOUT_TIMEOUT_SECONDS_RAW)
	if err != nil {
		return nil, fmt.Errorf("unable to parse environment variable as integer: %v", err)
	}
	NB_BUGOUT_TIMEOUT_SECONDS := time.Duration(bugoutTimeoutSeconds) * time.Second

	bugoutClient := bugout.ClientBrood(BUGOUT_BROOD_URL, NB_BUGOUT_TIMEOUT_SECONDS)
	return &bugoutClient, nil
}

func CheckEnvVarSet() {
	if NB_ACCESS_ID_HEADER == "" {
		NB_ACCESS_ID_HEADER = "x-node-balancer-access-id"
	}
	if NB_DATA_SOURCE_HEADER == "" {
		NB_DATA_SOURCE_HEADER = "x-node-balancer-data-source"
	}
	_, err := uuid.Parse(NB_CONTROLLER_ACCESS_ID)
	if err != nil {
		NB_CONTROLLER_ACCESS_ID = uuid.New().String()
		log.Printf("Access ID for internal usage in NB_CONTROLLER_ACCESS_ID environment variable is not valid uuid, generated random one: %v", NB_CONTROLLER_ACCESS_ID)
	}
	for _, o := range strings.Split(MOONSTREAM_CORS_ALLOWED_ORIGINS, ",") {
		CORS_WHITELIST_MAP[o] = true
	}

	// Health check variables
	if NB_HEALTH_CHECK_INTERVAL_RAW != "" {
		healthCheckInterval, atoiErr := strconv.Atoi(NB_HEALTH_CHECK_INTERVAL_RAW)
		if atoiErr != nil {
			log.Printf("Unable to parse environment variable NB_HEALTH_CHECK_INTERVAL as integer and set to default %d, err: %v", NB_HEALTH_CHECK_INTERVAL, atoiErr)
		} else {
			NB_HEALTH_CHECK_INTERVAL = healthCheckInterval
		}
	}

	// Cache variables
	if NB_CACHE_CLEANING_INTERVAL_RAW != "" {
		nbCacheCleaningInterval, atoiErr := strconv.Atoi(NB_CACHE_CLEANING_INTERVAL_RAW)
		if atoiErr != nil {
			log.Printf("Unable to parse environment variable NB_CACHE_CLEANING_INTERVAL as integer and set to default %d, err: %v", NB_CACHE_CLEANING_INTERVAL, atoiErr)
		} else {
			NB_CACHE_CLEANING_INTERVAL = nbCacheCleaningInterval
		}
	}

	if NB_CACHE_ACCESS_ID_LIFETIME_RAW != "" {
		nbCacheAccessIdLifetime, atoiErr := strconv.Atoi(NB_CACHE_ACCESS_ID_LIFETIME_RAW)
		if atoiErr != nil {
			log.Printf("Unable to parse environment variable NB_CACHE_ACCESS_ID_LIFETIME as integer and set to default %d, err: %v", NB_CACHE_ACCESS_ID_LIFETIME, atoiErr)
		} else {
			NB_CACHE_ACCESS_ID_LIFETIME = int64(nbCacheAccessIdLifetime)
		}
	}

	if NB_CACHE_ACCESS_ID_SESSION_LIFETIME_RAW != "" {
		nbCacheAccessIdSessionLifetime, atoiErr := strconv.Atoi(NB_CACHE_ACCESS_ID_SESSION_LIFETIME_RAW)
		if atoiErr != nil {
			log.Printf("Unable to parse environment variable NB_CACHE_ACCESS_ID_SESSION_LIFETIME as integer and set to default %d, err: %v", NB_CACHE_ACCESS_ID_SESSION_LIFETIME, atoiErr)
		} else {
			NB_CACHE_ACCESS_ID_SESSION_LIFETIME = int64(nbCacheAccessIdSessionLifetime)
		}
	}
}

// Nodes configuration
type NodeConfig struct {
	Blockchain string `json:"blockchain"`
	Endpoint   string `json:"endpoint"`
}

func LoadConfig(configPath string) error {
	rawBytes, err := ioutil.ReadFile(configPath)
	if err != nil {
		return err
	}
	nodeConfigsTemp := &[]NodeConfig{}
	err = json.Unmarshal(rawBytes, nodeConfigsTemp)
	if err != nil {
		return err
	}
	nodeConfigs = *nodeConfigsTemp
	return nil
}

type ConfigPlacement struct {
	ConfigDirPath   string
	ConfigDirExists bool

	ConfigPath   string
	ConfigExists bool
}

func CheckPathExists(path string) (bool, error) {
	var exists = true
	_, err := os.Stat(path)
	if err != nil {
		if os.IsNotExist(err) {
			exists = false
		} else {
			return exists, fmt.Errorf("error due checking file path exists, err: %v", err)
		}
	}

	return exists, nil
}

func GetConfigPath(providedPath string) (*ConfigPlacement, error) {
	var configDirPath, configPath string
	if providedPath == "" {
		homeDir, err := os.UserHomeDir()
		if err != nil {
			return nil, fmt.Errorf("unable to find user home directory, %v", err)
		}
		configDirPath = fmt.Sprintf("%s/.nodebalancer", homeDir)
		configPath = fmt.Sprintf("%s/config.json", configDirPath)
	} else {
		configPath = strings.TrimSuffix(providedPath, "/")
		configDirPath = filepath.Dir(configPath)
	}

	configDirPathExists, err := CheckPathExists(configDirPath)
	if err != nil {
		return nil, err
	}
	configPathExists, err := CheckPathExists(configPath)
	if err != nil {
		return nil, err
	}

	config := &ConfigPlacement{
		ConfigDirPath:   configDirPath,
		ConfigDirExists: configDirPathExists,

		ConfigPath:   configPath,
		ConfigExists: configPathExists,
	}

	return config, nil
}

func GenerateDefaultConfig(config *ConfigPlacement) error {
	if !config.ConfigDirExists {
		if err := os.MkdirAll(config.ConfigDirPath, os.ModePerm); err != nil {
			return fmt.Errorf("unable to create directory, %v", err)
		}
		log.Printf("Config directory created at: %s", config.ConfigDirPath)
	}

	if !config.ConfigExists {
		tempConfig := []NodeConfig{
			{Blockchain: "ethereum", Endpoint: "http://127.0.0.1:8545"},
		}
		tempConfigJson, err := json.Marshal(tempConfig)
		if err != nil {
			return fmt.Errorf("unable to marshal configuration data, err: %v", err)
		}
		err = ioutil.WriteFile(config.ConfigPath, tempConfigJson, os.ModePerm)
		if err != nil {
			return fmt.Errorf("unable to write default config to file %s, err: %v", config.ConfigPath, err)
		}
		log.Printf("Created default configuration at %s", config.ConfigPath)
	}

	return nil
}

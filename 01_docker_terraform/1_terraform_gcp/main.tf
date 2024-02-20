terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.16.0"
    }
  }
}

provider "google" {
  # Configuration options
  project = "teak-spot-413208"
  region  = "asia-southeast1-b"
}


resource "google_storage_bucket" "demo-bucket" {
  name          = "arcsle09plus-bucket"
  location      = "ASIA"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 3
    }
    action {
      type = "Delete"
    }
  }

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

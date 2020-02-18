# get all fuel subtypes
query {
	allFuelSubTypes{
    pageInfo {
      startCursor,
      endCursor,
      hasPreviousPage,
      hasNextPage
    }
    edges {
      node {
        id,
        label,
        fuelType {
          id,
          code,
          label
        }
      }
    }
  }
}
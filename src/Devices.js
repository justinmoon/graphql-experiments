import React, { Component } from "react";
import { Query } from "react-apollo";
import gql from "graphql-tag";

const QUERY = gql`
  {
    devices {
      fingerprint
    }
  }
`;

const SUBSCRIPTION = gql`
  subscription {
    devices {
      fingerprint
    }
  }
`;

class Devices extends Component {
  componentDidMount() {
    this.props.subscribeToNewData();
  }

  render() {
    const { data, error, loading } = this.props;
    console.log(data)
    if (loading) return <p> Loading ... </p>;
    if (error) return <p>Error!</p>;
    return (
      <p>Devices: {JSON.stringify(data)}% </p>
    )
  }
}

const ConnectedDevices = () => (
  <Query query={QUERY}>
    {({ subscribeToMore, ...result }) => (
      <Devices
        {...result}
        subscribeToNewData={() =>
          subscribeToMore({
            document: SUBSCRIPTION,
            updateQuery: (prev, { subscriptionData }) => {
              console.log(prev, subscriptionData)
              if (!subscriptionData.data) return prev;
              return subscriptionData.data;
            }
          })
        }
      />
    )}
  </Query>
)

export default ConnectedDevices;

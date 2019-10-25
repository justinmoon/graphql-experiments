import React, { Component } from "react";
import { Query } from "react-apollo";
import gql from "graphql-tag";

const QUERY = gql`
  {
    nodes {
      online
    }
  }
`;

const SUBSCRIPTION = gql`
  subscription {
    nodes {
      online
    }
  }
`;

class Nodes extends Component {
  componentDidMount() {
    this.props.subscribeToNewData();
  }

  render() {
    const { data, error, loading } = this.props;
    console.log(data)
    if (loading) return <p> Loading ... </p>;
    if (error) return <p>Error!</p>;
    return (
      <p>Nodes: {JSON.stringify(data)}% </p>
    )
  }
}

const ConnectedNodes = () => (
  <Query query={QUERY}>
    {({ subscribeToMore, ...result }) => (
      <Nodes
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

export default ConnectedNodes;

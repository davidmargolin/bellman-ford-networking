import click
import csv

@click.command()
@click.argument('start_node')
@click.argument('input_graph', type=click.Path(exists=True))
@click.argument('output_path')
def cli_command(start_node, input_graph, output_path):
    nodes = {}
    # import graph from csv
    with open(input_graph) as graphfile:
        reader = csv.DictReader(graphfile)
        for row in reader:
            dest_cost_tup = (row["destination"], float(row["cost"]))
            if row["source"] in nodes:
                nodes[row["source"]].append(dest_cost_tup)
            else:
                nodes[row["source"]] = [dest_cost_tup]

    # initialize bellman-ford
    costs = {}
    for node in nodes:
        costs[node] = {"cost": "inf"}
    costs[start_node] = {"cost": 0, "via": "start"}

    click.echo(",".join(costs))
    click.echo(",".join(str(value["cost"]) for value in costs.values()))

    # iterate v-1 times
    count = 0
    while(count < len(costs) - 1):
        for node in nodes:
            if costs[node]["cost"] != "inf":
                for tup in nodes[node]:
                    destination = tup[0]
                    new_cost = costs[node]["cost"] + tup[1]
                    current_cost = costs[destination]["cost"]
                    if current_cost == "inf" or current_cost > new_cost:
                        costs[destination] = {
                            "cost": new_cost,
                            "via": node
                        }
        count += 1

        # print out current iteration
        click.echo(",".join(str(value["cost"]) for value in costs.values()))

    click.echo("\n")

    # write final costs
    with open(output_path, mode='w') as out_file:
        csv_writer = csv.writer(out_file)
        csv_writer.writerow(['dest', 'via', 'cost'])
        for node in costs:
            csv_writer.writerow([node, costs[node]["via"], costs[node]["cost"]])
    click.echo("\n".join("{}: {} via {}".format(key, str(value["cost"]), value["via"]) for (key, value) in costs.items()))

if __name__ == "__main__":
    cli_command()
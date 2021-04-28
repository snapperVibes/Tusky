export function concatUsername(username: string, number: string | bigint) {
  // concatUsername("Skrillex", 12) => "Skrillex#0012"
  //
  // concatUsername("Skrillex, "0012") => "Skrillex#0012"
  let _number: string
  if (typeof number === "string") {
    _number = number
  }
  else {
    _number = number.toString().padStart(4, "0")
  }
  return username + "#" + _number.toString().padStart(4, "0")
}

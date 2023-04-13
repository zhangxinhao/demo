package main

import (
	"fmt"
	"hello/morestrings"
	"rsc.io/quote"
)

func Hello() string {
	return quote.Hello()
}
func main() {
	fmt.Println("Hello, world.")
	fmt.Println(morestrings.ReverseRunes("!oG ,olleH"))
	fmt.Println(Hello())
}
